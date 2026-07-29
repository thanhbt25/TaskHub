import uuid

from app.database import Base
from app.models.enums import ProjectStatus
from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuiid64())
    )
    workspace_id = Column(
        String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        SQLEnum(ProjectStatus, native_enum=False),
        default=ProjectStatus.ACTIVE,
        nullable=False,
    )

    workspace = relationship("Workspace", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    labels = relationship(
        "Label", back_populates="project", cascade="all, delete-orphan"
    )
