from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Label(Base):
    __tablename__ = "labels"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    color = Column(String(20), default="#000000", nullable=True)

    project = relationship("Project", back_populates="labels")
    tasks = relationship("Label", secondary="task_labels", back_populates="labels")