from fastapi import HTTPException, status

from app.models.label import Label
from app.models.user import User
from app.repositories.label_repo import LabelRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.label import LabelCreate


class LabelService:
    def __init__(
        self,
        label_repo: LabelRepository,
        task_repo: TaskRepository,
    ):
        self.label_repo = label_repo
        self.task_repo = task_repo

    def create_label(self, current_user: User, dto: LabelCreate) -> Label:
        return self.label_repo.create(dto)

    def get_labels_by_project(
        self, project_id: str, current_user: User
    ) -> list[Label]:
        return self.label_repo.get_by_project(project_id)

    def assign_label(self, task_id: str, label_id: str, current_user: User) -> dict:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        label = self.label_repo.get_by_id(label_id)
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Label not found",
            )

        if label in task.labels:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Label already assigned to this task",
            )

        self.task_repo.add_label(task, label)
        return {"message": "Label assigned successfully"}

    def remove_label(self, task_id: str, label_id: str, current_user: User) -> None:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        label = self.label_repo.get_by_id(label_id)
        if not label or label not in task.labels:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Label not found or not assigned to this task",
            )

        self.task_repo.remove_label(task, label)