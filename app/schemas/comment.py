from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    parent_id: str | None = None

class CommentCreate(CommentBase):
    author_id: str | None = None

class CommentResponse(CommentBase):
    id: str
    task_id: str
    author_id: str | None
    created_at: datetime
    replies: list[CommentResponse] = []

    class Config:
        from_attributes = True