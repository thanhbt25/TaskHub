from fastapi import HTTPException, status

from app.models.enums import ProjectStatus, WorkspaceRole
from app.models.project import Project
from app.models.user import User
from app.repositories.project_repo import ProjectRepository
from app.repositories.workspace_repo import WorkspaceRepository
from app.schemas.project import ProjectCreateRequest, ProjectUpdateRequest


class ProjectService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        workspace_repo: WorkspaceRepository,
    ):
        self.project_repo = project_repo
        self.workspace_repo = workspace_repo

    def _check_workspace_access(
        self,
        workspace_id: str,
        user_id: str,
        required_roles: list[WorkspaceRole] | None = None,
    ):
        workspace = self.workspace_repo.get_by_id(workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found",
            )

        member = self.workspace_repo.get_member(workspace_id, user_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this workspace",
            )

        if required_roles and member.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have enough permission in this workspace",
            )

        return workspace, member

    def create_project(
        self, workspace_id: str, current_user: User, dto: ProjectCreateRequest
    ) -> Project:
        # Kiểm tra quyền: Phải là OWNER hoặc EDITOR của Workspace
        self._check_workspace_access(
            workspace_id,
            str(current_user.id),  # Ép kiểu về str
            [WorkspaceRole.OWNER, WorkspaceRole.EDITOR],
        )

        project = Project(
            workspace_id=workspace_id,
            name=dto.name,
            description=dto.description,
            status=ProjectStatus.ACTIVE,
        )
        return self.project_repo.create(project)

    def get_projects_by_workspace(
        self,
        workspace_id: str,
        current_user: User,
        status_filter: ProjectStatus | None = None,
    ) -> list[Project]:
        # Tất cả thành viên Workspace đều được xem danh sách Project
        self._check_workspace_access(workspace_id, str(current_user.id)) # Ép kiểu về str
        return self.project_repo.get_all_by_workspace(workspace_id, status_filter)

    def get_project_detail(self, project_id: str, current_user: User) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        self._check_workspace_access(str(project.workspace_id), str(current_user.id)) # Ép kiểu về str
        return project

    def update_project(
        self, project_id: str, current_user: User, dto: ProjectUpdateRequest
    ) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        self._check_workspace_access(
            str(project.workspace_id), # Ép kiểu về str
            str(current_user.id),      # Ép kiểu về str
            [WorkspaceRole.OWNER, WorkspaceRole.EDITOR],
        )

        update_data = dto.model_dump(exclude_unset=True)
        if not update_data:
            return project

        return self.project_repo.update(project, update_data)

    def archive_project(self, project_id: str, current_user: User) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        self._check_workspace_access(
            str(project.workspace_id), # Ép kiểu về str
            str(current_user.id),      # Ép kiểu về str
            [WorkspaceRole.OWNER, WorkspaceRole.EDITOR],
        )

        # Chuyển trạng thái sang ARCHIVED
        return self.project_repo.update(project, {"status": ProjectStatus.ARCHIVED})

    def delete_project(self, project_id: str, current_user: User) -> None:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        self._check_workspace_access(
            str(project.workspace_id), # Ép kiểu về str
            str(current_user.id),      # Ép kiểu về str
            [WorkspaceRole.OWNER, WorkspaceRole.EDITOR],
        )

        self.project_repo.delete(project)