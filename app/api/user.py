from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import ChangePasswordRequest, UserResponse, UserUpdateRequest
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


# Dependency Injector cho UserService
def get_user_service(db: Annotated[Session, Depends(get_db)]) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)


@router.patch("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_my_profile(
    update_data: UserUpdateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """
    Cập nhật thông tin cá nhân của User đang đăng nhập (Partial Update)
    """
    return user_service.update_profile(current_user, update_data)


@router.post("/me/change-password", status_code=status.HTTP_200_OK)
def change_password(
    dto: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """
    POST /api/v1/users/me/change-password - Đổi mật khẩu cho User đang đăng nhập
    """
    user_service.change_password(current_user, dto)
    return {"message": "Đổi mật khẩu thành công"}
