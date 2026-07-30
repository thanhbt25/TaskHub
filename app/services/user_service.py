from fastapi import HTTPException, status
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserUpdateRequest, ChangePasswordRequest
from app.models.user import User
from app.core.exceptions import ErrorMessages
from app.core.security import verify_password, hash_password

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def update_profile(self, current_user: User, update_dto: UserUpdateRequest) -> User:
        # 1. Trích xuất các trường thực sự được client gửi lên (bỏ qua các trường None)
        update_data = update_dto.model_dump(exclude_unset=True)

        if not update_data:
            return current_user # Không có gì thay đổi

        # 2. Kiểm tra nghiệp vụ: Nếu cập nhật Email, check xem email mới đã tồn tại chưa
        if "email" in update_data and update_data["email"] != current_user.email:
            existing_user = self.user_repo.get_by_email(update_data["email"])
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessages.EXISTED_EMAIL
                )

        # 3. Gọi Repo để cập nhật vào Database
        return self.user_repo.update(current_user, update_data)

    def change_password(self, current_user: User, dto: ChangePasswordRequest) -> None:
        # 1. Kiểm tra mật khẩu hiện tại có chính xác không
        if not verify_password(dto.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.NOT_TRUE_PASSWORD,
            )

        # 2. Băm (hash) mật khẩu mới
        new_hashed_password = hash_password(dto.new_password)

        # 3. Cập nhật vào DB
        self.user_repo.update_password(current_user, new_hashed_password)