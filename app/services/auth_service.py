from fastapi import HTTPException, status

from app.core.exceptions import ErrorMessages
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repo import UserRepository
from app.schemas.auth import TokenResponse, UserRegisterRequest


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, user_data: UserRegisterRequest):
        existing_user = self.user_repo.get_by_email_or_username(
            user_data.email, user_data.username
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.EXISTED_EMAIL,
            )

        hashed_pwd = hash_password(user_data.password)
        return self.user_repo.create_user(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_pwd,
        )

    def authenticate_user(self, username: str, password: str) -> TokenResponse:
        user = self.user_repo.get_by_username(username=username)
        if not user or not verify_password(password, str(user.hashed_password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessages.WRONG_EMAIL_OR_PASSWORD,
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "username": user.username}
        )

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
