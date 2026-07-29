import uuid

from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Comment(Base):
    __tablename__ = "comments"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuiid64())
    )
    task_id = Column(
        String(36), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    author_id = Column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    content = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")
