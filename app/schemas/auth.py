from pydantic import BaseModel, EmailStr

"""
BaseModel từ Pydantic được dùng làm Data Schema/DTO cho: 
- validate dữ liệu từ client lên server (HTTP Request Body)
- format dữ liệu đầu ra cho client 
- tự động sinh tài liệu api 

Khi nào dùng from_attributes ?
- dùng cho schema nhận dữ liệu đầu vào là một ORM model -> để lọc thông tin 
- không cần dùng khi là: Request Schema, Response Schema tạo thủ công, không lấy từ ORM model 
"""


class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str

    class Config:  # cho phép pydantic đọc DL trực tiếp từ đối tượng Python thông qua attributes chứ không chỉ từ dictionary
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    refresh_token: str
