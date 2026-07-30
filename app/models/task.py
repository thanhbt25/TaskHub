import uuid

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import TaskStatus


# quan hệ 1 - n thì cái n sẽ phải lấy id của 1 vào trong class, còn relationshiip thì 2 bên bảng đều phải viết
class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    project_id = Column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    assignee_id = Column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        SQLEnum(TaskStatus, native_enum=False),
        default=TaskStatus.TODO,
        nullable=False,
    )
    priority = Column(String(50), default="MEDIUM", nullable=True)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")
    comments = relationship(
        "Comment", back_populates="task", cascade="all, delete-orphan"
    )
    labels = relationship("Label", secondary="task_labels", back_populates="tasks")
