from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.repositories.label_repo import LabelRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.label import LabelCreate, LabelResponse
from app.services.label_service import LabelService

router = APIRouter(tags=["Labels"])


def get_label_service(db: Annotated[Session, Depends(get_db)]) -> LabelService:
    label_repo = LabelRepository(db)
    task_repo = TaskRepository(db)
    return LabelService(label_repo, task_repo)


@router.post(
    "/labels",
    response_model=LabelResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_label(
    dto: LabelCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LabelService, Depends(get_label_service)],
):
    """Tạo mới một Label"""
    return service.create_label(current_user, dto)


@router.get(
    "/projects/{project_id}/labels",
    response_model=list[LabelResponse],
    status_code=status.HTTP_200_OK,
)
def get_project_labels(
    project_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LabelService, Depends(get_label_service)],
):
    """Lấy danh sách Labels của một Project"""
    return service.get_labels_by_project(project_id, current_user)


@router.post(
    "/tasks/{task_id}/labels/{label_id}",
    status_code=status.HTTP_200_OK,
)
def assign_label(
    task_id: str,
    label_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LabelService, Depends(get_label_service)],
):
    """Gắn một Label vào Task"""
    return service.assign_label(task_id, label_id, current_user)


@router.delete(
    "/tasks/{task_id}/labels/{label_id}",
    status_code=status.HTTP_200_OK,
)
def remove_label(
    task_id: str,
    label_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LabelService, Depends(get_label_service)],
):
    """Gỡ một Label khỏi Task"""
    service.remove_label(task_id, label_id, current_user)
    return {"message": "Label removed successfully"}