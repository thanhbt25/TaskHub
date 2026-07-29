class ErrorMessages:
    # Lỗi phân quyền
    FORBIDDEN_ACTION = "You do not have enough permissions to perform this action"
    ROLE_NOT_ALLOWED = "Your role is not allowed to access this resource"
    CREDENTIALS = "Could not validate credentials"
    
    # Lỗi xác thực
    NOT_AUTHENTICATED = "Not authenticated"
    USER_NOT_FOUND = "User not found"
    TOKEN_EXPIRED = "Token has expired"
    
    # Lỗi dữ liệu khác
    PROJECT_NOT_FOUND = "Project description or ID not found"
    EXISTED_EMAIL = "Email existed in database"
    WRONG_EMAIL_OR_PASSWORD = "Invalid password or email"
    INACTIVE_USER="User is not active"

