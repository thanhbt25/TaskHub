import math

from fastapi import HTTPException, status, BackgroundTasks

from app.core.redis import CacheService
from app.models.enums import TaskPriority, TaskStatus, WorkspaceRole
from app.models.task import Task
from app.models.user import User
from app.repositories.project_repo import ProjectRepository
from app.repositories.task_repo import TaskRepository
from app.repositories.workspace_repo import WorkspaceRepository
from app.repositories.user_repo import UserRepository
from app.schemas.task import (
    PaginatedResponse,
    TaskCreateRequest,
    TaskResponse,
    TaskUpdateRequest,
)

from app.services.email_service import EmailService 


class TaskService:
    def __init__(
        self,
        task_repo: TaskRepository,
        project_repo: ProjectRepository,
        workspace_repo: WorkspaceRepository,
        user_repo: UserRepository, 
        email_service: EmailService
    ):
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.workspace_repo = workspace_repo
        self.user_repo = user_repo
        self.email_service = email_service

    def _verify_project_access(
        self,
        project_id: str,
        user_id: str,
        required_roles: list[WorkspaceRole] | None = None,
    ):
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        member = self.workspace_repo.get_member(str(project.workspace_id), user_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project",
            )

        if required_roles and member.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have enough permission",
            )

        return project

    def create_task(
        self, project_id: str, current_user: User, dto: TaskCreateRequest, background_tasks: BackgroundTasks
    ) -> Task:
        self._verify_project_access(
            project_id,
            str(current_user.id),
            [WorkspaceRole.OWNER, WorkspaceRole.EDITOR],
        )

        task = Task(
            project_id=project_id,
            title=dto.title,
            description=dto.description,
            assignee_id=dto.assignee_id,
            priority=dto.priority,
            due_date=dto.due_date,
        )

        created_task = self.task_repo.create(task)

        # 2. Kiểm tra User được gán có tồn tại không
        assignee = self.user_repo.get_by_id(str(dto.assignee_id))
        if assignee:
            if str(assignee.email):
                background_tasks.add_task(
                    self.email_service.send_task_assignment_email,
                    to_email=str(assignee.email),
                    task_title=str(created_task.title),
                    assignee_name=str(assignee.username)
                )
  
        # Xóa Cache danh sách task của Project này
        CacheService.delete_pattern(f"project_tasks:{project_id}:*")
        return created_task

    def get_project_tasks(
        self,
        project_id: str,
        current_user: User,
        status_filter: TaskStatus | None = None,
        priority_filter: TaskPriority | None = None,
        assignee_id: str | None = None,
        search: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> PaginatedResponse[TaskResponse]:
        self._verify_project_access(project_id, str(current_user.id))

        # Xây dựng Key Cache unique theo param
        cache_key = (
            f"project_tasks:{project_id}:st={status_filter}:pr={priority_filter}:"
            f"as={assignee_id}:q={search}:p={page}:s={size}"
        )

        cached_data = CacheService.get(cache_key)
        if cached_data:
            return PaginatedResponse[TaskResponse](**cached_data)

        tasks, total = self.task_repo.get_filtered_tasks(
            project_id=project_id,
            status=status_filter,
            priority=priority_filter,
            assignee_id=assignee_id,
            search=search,
            page=page,
            size=size,
        )

        total_pages = math.ceil(total / size) if total > 0 else 0
        task_dtos = [TaskResponse.model_validate(task) for task in tasks]

        result = PaginatedResponse[TaskResponse](
            items=task_dtos,
            total=total,
            page=page,
            size=size,
            total_pages=total_pages,
        )

        # Lưu Cache trong 300s (5 phút)
        CacheService.set(cache_key, result.model_dump(), ttl_seconds=300)
        return result

    def update_task(
        self, task_id: str, current_user: User, dto: TaskUpdateRequest
    ) -> Task:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        self._verify_project_access(
            str(task.project_id),
            str(current_user.id),
            [WorkspaceRole.OWNER, WorkspaceRole.EDITOR],
        )

        update_data = dto.model_dump(exclude_unset=True)
        if not update_data:
            return task

        updated_task = self.task_repo.update(task, update_data)
        CacheService.delete_pattern(f"project_tasks:{task.project_id}:*")
        return updated_task

    def delete_task(self, task_id: str, current_user: User) -> None:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        self._verify_project_access(
            str(task.project_id),
            str(current_user.id),
            [WorkspaceRole.OWNER, WorkspaceRole.EDITOR],
        )

        project_id = task.project_id
        self.task_repo.delete(task)
        CacheService.delete_pattern(f"project_tasks:{project_id}:*")

    def assign_task(
        self, 
        task_id: str, 
        assignee_id: str, 
        current_user: User, 
        background_tasks: BackgroundTasks
    ) -> Task:
        # 1. Kiểm tra Task có tồn tại không
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        # 2. Kiểm tra User được gán có tồn tại không
        assignee = self.user_repo.get_by_id(assignee_id)
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignee not found",
            )

        # 3. Cập nhật Task với người được gán mới
        updated_task = self.task_repo.update(task, {"assignee_id": assignee.id})

        # 4. Thêm tác vụ gửi email vào BackgroundTasks (Chạy ngầm không block API)
        if str(assignee.email):
            background_tasks.add_task(
                self.email_service.send_task_assignment_email,
                to_email=str(assignee.email),
                task_title=str(updated_task.title),
                assignee_name=str(assignee.username)
            )

        return updated_task
