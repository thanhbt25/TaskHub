from typing import Any

from sqlalchemy.orm import Session

from app.models.enums import TaskPriority, TaskStatus
from app.models.task import Task
from app.models.label import Label


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: str) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_filtered_tasks(
        self,
        project_id: str,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        assignee_id: str | None = None,
        search: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> tuple[list[Task], int]:
        query = self.db.query(Task).filter(Task.project_id == project_id)

        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        if assignee_id:
            query = query.filter(Task.assignee_id == assignee_id)
        if search:
            query = query.filter(Task.title.ilike(f"%{search}%"))

        total = query.count()
        offset = (page - 1) * size
        tasks = query.offset(offset).limit(size).all()

        return tasks, total

    def update(self, task: Task, update_data: dict[str, Any]) -> Task:
        for key, value in update_data.items():
            setattr(task, key, value)

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()

    def add_label(self, task: Task, label: Label):
        task.labels.append(label)
        self.db.commit()

    def remove_label(self, task: Task, label: Label):
        task.labels.remove(label)
        self.db.commit()
