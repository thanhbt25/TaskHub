from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import ProjectStatus


class ProjectCreateRequest(BaseModel):
    name: str
    description: str | None = None


class ProjectUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None


class ProjectResponse(BaseModel):
    id: str
    workspace_id: str
    name: str
    description: str | None = None
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
