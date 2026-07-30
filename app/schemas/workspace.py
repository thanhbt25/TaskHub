from datetime import datetime
from typing import List, Optional

from app.models.enums import WorkspaceRole
from app.schemas.user import UserResponse
from pydantic import BaseModel, ConfigDict


class WorkspaceCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class AddMemberRequest(BaseModel):
    user_id: str
    role: WorkspaceRole = WorkspaceRole.VIEWER


class WorkspaceMemberResponse(BaseModel):
    user_id: str
    role: WorkspaceRole
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    owner_id: str
    created_at: datetime
    members: List[WorkspaceMemberResponse] = []

    model_config = ConfigDict(from_attributes=True)

class WorkspaceUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None