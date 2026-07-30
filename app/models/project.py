import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.models.enums import ProjectStatus

"""
Các chế độ cascade: 
- save-update: db.add() bảng cha vào session -> tất cả bảng con tự động được thêm vào session 
- delete: khi xóa bảng cha, tất cả bảng con đều bị xóa theo 
- delete-orphan: khi một bảng con bị gỡ quan hệ bảng cha(mồ côi) -> tự động bị xóa 
- refresh-expire: khi db.refresh() hoặc làm hết hạn DL bảng cha, bảng con cũng được mới theo 
- merge: db.merge() bảng cha từ session cũ sang mới -> bảng con cũng gộp theo 
- all: = save-update, merge, refresh-expire, expunge, delete (không bao gồm delete-orphan)
"""


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
    )
    
    workspace = relationship("Workspace", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    labels = relationship(
        "Label", back_populates="project", cascade="all, delete-orphan"
    )
