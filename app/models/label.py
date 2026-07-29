import uuid

from app.database import Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

# relationship: không tạo cột mới, tạo liên kết giữa các object -> task.project 
# back_populates -> bên kia đặt biến class này là gì 

class Label(Base):
    __tablename__ = "labels" # đặt tên bảng, hiển thị trong CSDL

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    ) # đặt cột này làm index -> tìm kiếm nhanh hơn, default -> nếu không tự đặt thì tự sinh 
    project_id = Column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(100), nullable=False)
    color = Column(String(20), default="#000000", nullable=True)

    project = relationship("Project", back_populates="labels")
    tasks = relationship("Task", secondary="task_labels", back_populates="labels")
