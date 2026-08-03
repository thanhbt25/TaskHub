from fastapi import HTTPException, status

from app.models.comment import Comment
from app.models.user import User
from app.repositories.comment_repo import CommentRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.comment import CommentCreate


class CommentService:
    def __init__(
        self,
        comment_repo: CommentRepository,
        task_repo: TaskRepository,
    ):
        self.comment_repo = comment_repo
        self.task_repo = task_repo

    def create_comment(
        self, task_id: str, current_user: User, dto: CommentCreate
    ) -> Comment:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        if dto.parent_id:
            parent = self.comment_repo.get_by_id(dto.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent comment not found",
                )
            
            if str(parent.task_id) != str(task_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Parent comment does not belong to this task",
                )

        # Gắn author_id là user hiện tại
        dto.author_id = str(current_user.id)
        return self.comment_repo.create(task_id, dto)

    def get_comments(self, task_id: str, current_user: User) -> list[Comment]:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
            
        return self.comment_repo.get_root_comments(task_id)