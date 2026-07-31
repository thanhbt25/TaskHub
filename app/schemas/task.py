from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TaskPriority, TaskStatus

T = TypeVar("T")


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    assignee_id: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None


class TaskUpdateRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    assignee_id: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    id: str
    project_id: str
    assignee_id: str | None = None
    title: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse[T](BaseModel):
    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int
