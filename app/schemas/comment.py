from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    parent_id: Optional[str] = None

class CommentCreate(CommentBase):
    author_id: Optional[str] = None

class CommentResponse(CommentBase):
    id: str
    task_id: str
    author_id: Optional[str]
    created_at: datetime
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True