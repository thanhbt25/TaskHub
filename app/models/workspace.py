import uuid

from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuiid64())
    )
    name = Column(String(255), nullable=False)
    owner_id = Column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    owner = relationship("User", back_populates="owned_workspaces")
    members = relationship(
        "WorkspaceMember", back_populates="workspace", cascade="all, delete-orphan"
    )
    projects = relationship(
        "Project", back_populates="workspace", cascade="all, delete-orphan"
    )
