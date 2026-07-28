from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import TaskStatus
import uuid 

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuiid64()))
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    assignee_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
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
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    labels = relationship("Label", secondary="task_labels", back_populates="tasks")