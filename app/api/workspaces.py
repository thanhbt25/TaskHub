from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.repositories.workspace_repo import WorkspaceRepository
from app.schemas.workspace import (
    AddMemberRequest,
    WorkspaceCreateRequest,
    WorkspaceMemberResponse,
    WorkspaceResponse,
)
from app.services.workspace_service import WorkspaceService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])


def get_workspace_service(db: Session = Depends(get_db)) -> WorkspaceService:
    repo = WorkspaceRepository(db)
    return WorkspaceService(repo)


@router.post(
    "", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED
)
def create_workspace(
    dto: WorkspaceCreateRequest,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(get_workspace_service),
):
    return service.create_workspace(current_user, dto)


@router.get(
    "/{id}", response_model=WorkspaceResponse, status_code=status.HTTP_200_OK
)
def get_workspace_detail(
    id: str,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(get_workspace_service),
):
    return service.get_workspace_detail(id, current_user)


@router.post(
    "/{id}/members",
    response_model=WorkspaceMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_workspace_member(
    id: str,
    dto: AddMemberRequest,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(get_workspace_service),
):
    return service.add_member(id, current_user, dto)


@router.delete("/{id}/members/{user_id}", status_code=status.HTTP_200_OK)
def remove_workspace_member(
    id: str,
    user_id: str,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(get_workspace_service),
):
    service.remove_member(id, current_user, user_id)
    return {"message": "Member removed successfully"}