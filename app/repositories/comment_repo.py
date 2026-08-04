from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment import CommentCreate


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_by_id(self, comment_id: str) -> Comment | None:
        return self.db.query(Comment).filter(Comment.id == comment_id).first()
    
    def create(self, task_id: str, payload: CommentCreate) -> Comment:
        new_comment = Comment(
            task_id=task_id,
            parent_id=payload.parent_id,
            content=payload.content,
            author_id=payload.author_id
        )
        self.db.add(new_comment)
        self.db.commit()
        self.db.refresh(new_comment)
        return new_comment

    def get_root_comments(self, task_id: str):
        return (
            self.db.query(Comment)
            .filter(Comment.task_id == task_id, Comment.parent_id.is_(None))
            .order_by(Comment.created_at.desc())
            .all()
        )