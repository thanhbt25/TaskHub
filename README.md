# TaskHub
## Mục tiêu 
- Hệ thống quản lý công việc
- Domain: User, Workspace, Project, Task, Label, Comment, Notification 

## DB Schema
[ERD DIAGRAM](https://mermaid.live/edit#pako:eNqtVstu2kAU_ZXRSNmRFJtX7F0anBZFgZREiVQhWYN9MdPYM9bMuHkQ1v2Oqh_QfbPsl-RPOnYM2MEg0tareZxz77mPuTDDHvcB2xhEl5JAkGgkRgzpL5EgJJottuk3pgFlClEfnZ8Wz6USlAUIIkLDivNJEoYuIxFU3E2JnILvxkTKWy78IgJYEiHBQ0AjfNQ96_XRO3TmnL13hiNcUsU1hjBEpUs8Rb-W3PhEgaIRIE-AXvouUYvrebpYbLTzGxkTD94W8uuocji_ZSBcTTo5_ScxbgTReFMZVqhMXe2VsxyVlrEaUMzv4LrvDHV-nW7vcpAurnrOdTHRJX2x4F_AUzumqkruyS7JzI99kJ6gsaKcrcmXiqhEpg1yfNm7crTwo-HxR73qbpCuiLx5m-482HXV-b3uXBow2ByWoiosxaXgTu0W1eWgO9Ax9fru-XDwYehcXLzshk5aH73uDvpO-TXkTmNBuaDqvjIJIRlD-J-ysL12Hg-52FgId4uQ7H5bY2fcdUTJicejCNgbG3XhubraiZryiqed1dTjTGl3f_Pk9_bQp0QPsenz0zcU0OennwR5v797aPz86wcLykP58XF_n8-KM8vWzaKHjlz1QjVyOVBSgs4fZ4FEiq9oBZtbuXpur0ibyctJkXLS9BDKKohLWE57eaVrfl7D8vZJcT5MKIMK06U8rOzmr9YvBV8eEgWOW_BUUpSfb4Du7mTZqGseSvpLsFvBFYwwruFAUB_bSiRQwxEI_TOst3iWGhhhNQX9NHGWJCJutGU215yYsM-cRwua4EkwxfaEhFLvkjjt2_wPwRICzAdxzBOmsN1oNMzMCLZn-A7b-4bRPDAadbPd6ViWaZimVcP36bnVOWhaDateN5odq61h8xp-yDybBw2jVT9sHRpWu21ardb8D66tslM)

1. users: id, email, username, hashed_password, role (ADMIN/MEMBER), is_active, created_at 
2. workspaces: id, name, owner_id, created_at
3. workspace_members: workspace_id, user_id, role (OWNER/EDITOR/VIEWER)
4. projects: id, workspace_id, name, description, status (ACTIVE/ARCHIVED)
5. tasks: id, project_id, assignee_id, title, description, status (TODO/IN_PROGRESS/IN_REVIEW/DONE), priority
6. labels: id, project_id, name, color 
7. task_labels: task_id, label_id
8. comments: id, task_id, author_id, content, created_at

## Features
1. Auth: Register, Login (JWT access + refresh token), Logout (revoke refresh token)
2. User: Get profile, Update profile (PATCH), Change password
3. Workspace: CRUD (owner only), invite member, remove member, phân quyền theo role 
4. project: CRUD trong workspace, archive project
5. tasks: crud trong project, assign task cho member, chuyển status, đặt priority & due date
6. label: crud (per project), gán/bỏ label cho task
7. comment: thêm/xóa comment trên task 
8. fitering & pagnination: lock task theo status, priority, assignee, page + limit 
9. caching: cache GET /projects/{id}/tasks với Redis, invalidate khi có sự thay đổi 
10. Background task: gửi email notification khi được assign task 
11. RBAC: phân quyền admin/owner/editor/viewer đúng theo từng resource 
12. Swagger/ReDoc đầy đủ, có Bearer auth scheme, document error response 
13. docker compose up chạy được toàn bộ stack (app + db + redis)
14. ruff lint pass 100%, mypy không có error 

## Endpoints
```
POST /api/v1/auth/register

POST /api/v1/auth/login

POST /api/v1/auth/refresh

POST /api/v1/auth/logout

GET /api/v1/users/me

PATCH /api/v1/users/me

POST /api/v1/workspaces

GET /api/v1/workspaces/{id}

POST /api/v1/workspaces/{id}/members

DELETE /api/v1/workspaces/{id}/members/{user_id}

POST /api/v1/workspaces/{id}/projects

GET /api/v1/projects/{id}/tasks (filter + pagination + cache)

POST /api/v1/projects/{id}/tasks

PATCH /api/v1/tasks/{id}

DELETE /api/v1/tasks/{id}

POST /api/v1/tasks/{id}/labels/{label_id}

POST /api/v1/tasks/{id}/comments
```

## Cấu trúc thư mục 
```
my_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Khởi tạo FastAPI app và kết nối routers
│   │
│   ├── core/                    # Cấu hình hệ thống hệ thống (Global)
│   │   ├── config.py            # Đọc file .env, cấu hình app
│   │   ├── database.py          # Khởi tạo kết nối DB (SessionLocal, Engine)
│   │   └── security.py          # Xử lý băm mật khẩu, JWT token
│   │
│   ├── api/                     # LAYER 1: API / Presentation Layer
│   │   ├── v1/
│   │   │   ├── api.py           # Gom tất cả các router của v1 lại
│   │   │   └── endpoints/
│   │   │       ├── users.py     # Endpoint quản lý User
│   │   │       └── items.py     # Endpoint quản lý Item
│   │   └── deps.py              # Các dependency dùng chung (get_db, get_current_user)
│   │
│   ├── schemas/                 # Pydantic Models (Validation dữ liệu API)
│   │   ├── user.py              # UserCreate, UserResponse, UserUpdate
│   │   └── item.py              # ItemCreate, ItemResponse
│   │
│   ├── services/                # LAYER 2: Business Logic Layer
│   │   ├── user_service.py      # Logic xử lý nghiệp vụ cho User
│   │   └── item_service.py      # Logic xử lý nghiệp vụ cho Item
│   │
│   ├── repositories/            # LAYER 3: Data Access Layer (CRUD)
│   │   ├── user_repo.py         # Truy vấn DB bảng User
│   │   └── item_repo.py         # Truy vấn DB bảng Item
│   │
│   └── models/                  # Database Models (SQLAlchemy / Tortoise ORM)
│       ├── user.py              # Định nghĩa bảng 'users' trong DB
│       └── item.py              # Định nghĩa bảng 'items' trong DB
│
├── migrations/                  # Thư mục chứa file migration của Alembic (nếu có)
├── .env                         # Lưu trữ biến môi trường (Database URL, Secret Key)
├── requirements.txt             # Danh sách thư viện Python cần cài đặt
└── README.md                    # Hướng dẫn dự án
```

## Chạy ứng dụng 
- Bất khi có sự thay đổi nào trong code thì server sẽ tự động khởi động lại 
- Nếu không cần, xóa --reload đi 
```
python -m uvicorn app.main:app --reload
```
- Quy tắc import app.(...), do chạy file từ folder TaskHub
- Vào http://127.0.0.1:8000/docs để xem Swagger 
- Chạy migrations: khi có sự thay đổi nào thì chạy cái này
```
# sinh file script ghi lại sự thay đổi 
uv run python -m alembic revision --autogenerate -m "Mô tả sự thay đổi"

# áp dụng thay đổi vào database (upgrade)
uv run python -m alembic upgrade head

# xem phiên bản DB hiện tại đang ở đâu 
uv run alembic current 

# xem toàn bộ lịch sử các bản migration 
uv run alembic history --verbose 

# lùi 1 phiên bản gần nhất
uv run alembic downgrade -1

# lùi hẳn về ban đầu (xóa sạch bảng)
uv run alembic downgrade base 
```

### Format code 
1. Format toàn bộ code 
```
uv format . # Cách 1
uv run ruff format . # Cách 2  
```
2. kiểm tra định dạng (có dòng nào lỗi format không)
```
uv format --check .
```
3. kiểm tra lỗi 
```
uv run ruff check . 
```
4. tự động sửa lỗi các lỗi có thể sửa 
```
uv run ruff check --fix . 
```

### Khởi động Redis 
- Sử dụng cho Task 
```
# Khi chưa có trong Docker 
docker run -d --name taskhub-redis -p 6379:6379 redis:alpine
# Gọi redis dậy trong Docker 
docker start taskhub-redis
# Check redis đã hoạt động chưa
python -c "import redis; r = redis.Redis(host='localhost', port=6379, socket_timeout=2); print('Kết nối thành công!' if r.ping() else 'Lỗi')"
```

# Chạy server từ docker 
```
# 1. gọi server dậy 
docker compose up -d --build

# 2. kiểm tra trạng thái Container, cột STATUS CỦA web và redis phải hiện chữ UP, nếu Exited nghĩa là có lỗi 
docker compose ps

# 3. xem log xem có thành công không, tương tác với server 
docker compose logs -f 
```
- Kiểm tra giao diện Swagger http://localhost:8000/docs xem có chạy không 
- Kiểm tra đọc/ghi DB và test Redis trên Swagger xem đã được chưa 


