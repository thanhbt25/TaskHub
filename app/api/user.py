from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserUpdateRequest, UserResponse
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

# Dependency Injector cho UserService
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)


@router.patch("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_my_profile(
    update_data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Cập nhật thông tin cá nhân của User đang đăng nhập (Partial Update)
    """
    return user_service.update_profile(current_user, update_data)