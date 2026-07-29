# repo là file làm việc trực tiếp với bảng users trong database 
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter((User.email == email)).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email_or_username(self, email: str, username: str) -> Optional[User]:
        return self.db.query(User).filter((User.email == email) | (User.username == username)).first()

    def create_user(self, email: str, username: str, hashed_password: str) -> User:
        user = User(email=email, username=username, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user) # cập nhật lại object user -> do chưa có ID sẵn 
        return user