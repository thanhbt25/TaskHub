from sqlalchemy.orm import Session

from app.models.label import Label
from app.schemas.label import LabelCreate


class LabelRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, label_id: str) -> Label | None:
        return self.db.query(Label).filter(Label.id == label_id).first()

    def create(self, payload: LabelCreate) -> Label:
        new_label = Label(
            project_id=payload.project_id,
            name=payload.name,
            color=payload.color
        )
        self.db.add(new_label)
        self.db.commit()
        self.db.refresh(new_label)
        return new_label

    def get_by_project(self, project_id: str) -> list[Label]:
        return self.db.query(Label).filter(Label.project_id == project_id).all()