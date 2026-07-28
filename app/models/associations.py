# chứa các bảng phụ N-N
from sqlalchemy import Column, BigInteger, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import WorkspaceRole

class TaskLabel(Base):
    __tablename__ = "task_labels"

    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    label_id = Column(BigInteger, ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True)

class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    workspace_id = Column(BigInteger, ForeignKey("workspaces.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role = Column(
        SQLEnum(WorkspaceRole, native_enum=False),
        default=WorkspaceRole.VIEWER,
        nullable=False,
    )

    workspace = relationship("Workspace", back_populates="members")
    user = relationship("User", back_populates="workspace_memberships")