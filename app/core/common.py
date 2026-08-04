from app.schemas.common import ErrorResponse
from typing import Any

# Định nghĩa các lỗi dùng chung
COMMON_ERRORS = {
    400: {"model": ErrorResponse, "description": "Bad Request - Dữ liệu không hợp lệ"},
    401: {"model": ErrorResponse, "description": "Unauthorized - Chưa đăng nhập hoặc Token hết hạn"},
    403: {"model": ErrorResponse, "description": "Forbidden - Không có quyền thực hiện hành động này"},
    404: {"model": ErrorResponse, "description": "Not Found - Không tìm thấy tài nguyên"},
    500: {"model": ErrorResponse, "description": "Internal Server Error - Lỗi hệ thống"},
}

# Có thể tạo thêm các bộ lỗi đặc thù cho từng module
GLOBAL_ERRORS: dict[int | str, dict[str, Any]] = {
    **COMMON_ERRORS, # Kế thừa các lỗi chung
    409: {"model": ErrorResponse, "description": "Conflict - Tên Project đã tồn tại"},
}