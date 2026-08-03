from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.repositories.comment_repo import CommentRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment_service import CommentService

router = APIRouter(tags=["Comments"])


def get_comment_service(db: Annotated[Session, Depends(get_db)]) -> CommentService:
    comment_repo = CommentRepository(db)
    task_repo = TaskRepository(db)
    return CommentService(comment_repo, task_repo)


@router.post(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    task_id: str,
    dto: CommentCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CommentService, Depends(get_comment_service)],
):
    """Tạo mới một Comment (hỗ trợ nested comment qua parent_id)"""
    return service.create_comment(task_id, current_user, dto)


@router.get(
    "/tasks/{task_id}/comments",
    response_model=list[CommentResponse],
    status_code=status.HTTP_200_OK,
)
def get_comments(
    task_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CommentService, Depends(get_comment_service)],
):
    """Lấy danh sách Comments của một Task"""
    return service.get_comments(task_id, current_user)