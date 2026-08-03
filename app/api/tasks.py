from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.enums import TaskPriority, TaskStatus
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
from app.services.task_service import TaskService
from app.services.label_service import LabelService
from app.services.email_service import EmailService

router = APIRouter(tags=["Tasks"])


def get_task_service(db: Annotated[Session, Depends(get_db)]) -> TaskService:
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    workspace_repo = WorkspaceRepository(db)
    user_repo = UserRepository(db)
    email_service = EmailService()
    return TaskService(task_repo, project_repo, workspace_repo, email_service=email_service, user_repo=user_repo)


@router.get(
    "/projects/{id}/tasks",
    response_model=PaginatedResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
)
def get_project_tasks(
    id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
    status_filter: Annotated[
        TaskStatus | None,
        Query(alias="status", description="Lọc theo status"),
    ] = None,
    priority_filter: Annotated[
        TaskPriority | None,
        Query(alias="priority", description="Lọc theo độ ưu tiên"),
    ] = None,
    assignee_id: Annotated[
        str | None,
        Query(description="Lọc theo người thực hiện"),
    ] = None,
    search: Annotated[
        str | None,
        Query(description="Tìm kiếm theo tiêu đề task"),
    ] = None,
    page: Annotated[int, Query(ge=1, description="Trang số")] = 1,
    size: Annotated[int, Query(ge=1, le=100, description="Kích thước trang")] = 10,
):
    """Lấy danh sách tasks trong Project (Hỗ trợ Filter, Pagination và Redis Cache)"""
    return service.get_project_tasks(
        project_id=id,
        current_user=current_user,
        status_filter=status_filter,
        priority_filter=priority_filter,
        assignee_id=assignee_id,
        search=search,
        page=page,
        size=size,
    )


@router.post(
    "/projects/{id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    id: str,
    dto: TaskCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    """Tạo Task mới thuộc Project"""
    return service.create_task(id, current_user, dto, background_tasks)


@router.patch(
    "/tasks/{id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
def update_task(
    id: str,
    dto: TaskUpdateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    """Cập nhật thông tin/trạng thái Task"""
    return service.update_task(id, current_user, dto)


@router.delete("/tasks/{id}", status_code=status.HTTP_200_OK)
def delete_task(
    id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    """Xóa Task"""
    service.delete_task(id, current_user)
    return {"message": "Task deleted successfully"}

@router.patch(
    "/tasks/{task_id}/assign/{assignee_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
def assign_task(
    task_id: str,
    assignee_id: str,
    background_tasks: BackgroundTasks, # <-- FastAPI tự inject cái này
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
):
    """Gán Task cho một User và gửi email thông báo ngầm"""
    # Chuyền background_tasks xuống tầng Service
    return service.assign_task(task_id, assignee_id, current_user, background_tasks)