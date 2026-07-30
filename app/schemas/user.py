from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)