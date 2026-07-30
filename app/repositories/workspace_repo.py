from typing import Any

from sqlalchemy.orm import Session

from app.models.associations import WorkspaceMember
from app.models.enums import WorkspaceRole
from app.models.workspace import Workspace


class WorkspaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, workspace: Workspace) -> Workspace:
        self.db.add(workspace)
        self.db.commit()
        self.db.refresh(workspace)
        return workspace

    def get_by_id(self, workspace_id: str) -> Workspace | None:
        return self.db.query(Workspace).filter(Workspace.id == workspace_id).first()

    def get_member(self, workspace_id: str, user_id: str) -> WorkspaceMember | None:
        return (
            self.db.query(WorkspaceMember)
            .filter(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == user_id,
            )
            .first()
        )

    def add_member(
        self, workspace_id: str, user_id: str, role: WorkspaceRole
    ) -> WorkspaceMember:
        member = WorkspaceMember(workspace_id=workspace_id, user_id=user_id, role=role)
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def remove_member(self, member: WorkspaceMember) -> None:
        self.db.delete(member)
        self.db.commit()

    def update(self, workspace: Workspace, update_data: dict[str, Any]) -> Workspace:
        for key, value in update_data.items():
            setattr(workspace, key, value)

        self.db.add(workspace)
        self.db.commit()
        self.db.refresh(workspace)
        return workspace

    def delete(self, workspace: Workspace) -> None:
        self.db.delete(workspace)
        self.db.commit()
