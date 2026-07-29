from typing import List 
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.models.user import User
from app.models.enums import SystemRole
from app.core.exceptions import ErrorMessages

'''
- HTTPException: trả về lỗi HTTP 
- Depends: cơ chế Dependency Injection của FastAPI
- status: chứa mã HTTP có sẵn như status.HTTP_401_UNAUTHORIZED -> 401 Unauthorized 
- OAuth2PasswordBearer: để lấy JWT token từ HTTP Header 
- payload gồm có sub (id người dùng), exp (thời gian hết hạn của token), iat (thời gian token được khởi tạo),...
'''

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorMessages.CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessages.INACTIVE_USER
        )

    return user

def refresh_token_deps(token_str: str):
    try:
        payload = jwt.decode(
            token_str, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Cấp access token mới
    new_access_token = create_access_token(data={"sub": user_id})
    return {"access_token": new_access_token, "token_type": "bearer"}

class RoleChecker:
    def __init__(self, allowed_roles: List[SystemRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorMessages.FORBIDDEN_ACTION,
            )
        return current_user

require_admin = RoleChecker([SystemRole.ADMIN])
require_member_or_admin = RoleChecker([SystemRole.ADMIN, SystemRole.MEMBER])

