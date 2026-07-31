from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.enums import ProjectStatus
from app.models.user import User
from app.repositories.project_repo import ProjectRepository
from app.repositories.workspace_repo import WorkspaceRepository
from app.schemas.project import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from app.services.project_service import ProjectService

router = APIRouter(tags=["Projects"])


def get_project_service(db: Annotated[Session, Depends(get_db)]) -> ProjectService:
    project_repo = ProjectRepository(db)
    workspace_repo = WorkspaceRepository(db)
    return ProjectService(project_repo, workspace_repo)


@router.post(
    "/workspaces/{workspace_id}/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    workspace_id: str,
    dto: ProjectCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """Tạo Project mới thuộc Workspace"""
    return service.create_project(workspace_id, current_user, dto)


@router.get(
    "/workspaces/{workspace_id}/projects",
    response_model=list[ProjectResponse],
    status_code=status.HTTP_200_OK,
)
def get_projects_by_workspace(
    workspace_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ProjectService, Depends(get_project_service)],
    status: Annotated[
        ProjectStatus | None, Query(description="Lọc theo trạng thái ACTIVE / ARCHIVED")
    ] = None,
):
    """Lấy danh sách tất cả các Projects trong Workspace (Có thể lọc theo status)"""
    return service.get_projects_by_workspace(workspace_id, current_user, status)


@router.get(
    "/projects/{id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def get_project_detail(
    id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """Lấy thông tin chi tiết một Project"""
    return service.get_project_detail(id, current_user)


@router.patch(
    "/projects/{id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def update_project(
    id: str,
    dto: ProjectUpdateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """Cập nhật tên hoặc mô tả của Project"""
    return service.update_project(id, current_user, dto)


@router.patch(
    "/projects/{id}/archive",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def archive_project(
    id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """Lưu trữ Project (Chuyển trạng thái sang ARCHIVED)"""
    return service.archive_project(id, current_user)


@router.delete("/projects/{id}", status_code=status.HTTP_200_OK)
def delete_project(
    id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """Xóa hoàn toàn Project khỏi hệ thống"""
    service.delete_project(id, current_user)
    return {"message": "Project deleted successfully"}
