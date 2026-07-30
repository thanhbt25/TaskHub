from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import WorkspaceRole
from app.schemas.user import UserResponse


class WorkspaceCreateRequest(BaseModel):
    name: str
    description: str | None = None


class AddMemberRequest(BaseModel):
    user_id: str
    role: WorkspaceRole = WorkspaceRole.VIEWER


class WorkspaceMemberResponse(BaseModel):
    user_id: str
    role: WorkspaceRole
    user: UserResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    owner_id: str
    created_at: datetime
    members: list[WorkspaceMemberResponse] = []

    model_config = ConfigDict(from_attributes=True)


class WorkspaceUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
