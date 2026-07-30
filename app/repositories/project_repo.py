from typing import Any, Dict, List, Optional
from app.models.enums import ProjectStatus
from app.models.project import Project
from sqlalchemy.orm import Session


class ProjectRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_all_by_workspace(
        self, workspace_id: str, status: Optional[ProjectStatus] = None
    ) -> List[Project]:
        query = self.db.query(Project).filter(Project.workspace_id == workspace_id)
        if status:
            query = query.filter(Project.status == status)
        return query.all()

    def update(self, project: Project, update_data: Dict[str, Any]) -> Project:
        for key, value in update_data.items():
            setattr(project, key, value)

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: Project) -> None:
        self.db.delete(project)
        self.db.commit()