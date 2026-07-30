
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserUpdateRequest(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1, description="Mật khẩu hiện tại")
    new_password: str = Field(
        ..., min_length=6, description="Mật khẩu mới (tối thiểu 6 ký tự)"
    )

    @model_validator(mode="after")
    def check_passwords_differ(self):
        if self.current_password == self.new_password:
            raise ValueError("Mật khẩu mới không được trùng với mật khẩu hiện tại")
        return self
