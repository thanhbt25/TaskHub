from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid 

class Comment(Base):
    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuiid64()))
    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")