from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.comments import router as comment_router
from app.api.labels import router as label_router
from app.api.projects import router as project_router
from app.api.tasks import router as task_router
from app.api.user import router as user_router
from app.api.workspaces import router as workspace_router
from app.database import Base, engine

PREFIX_API = "/api/v1"
# 1. Lệnh này sẽ tự động tạo file database.sqlite và các bảng (nếu có)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskHub API",
    description="Hệ thống quản lý công việc TaskHub API",
    version="1.0.0",
)

# Include router
app.include_router(auth_router, prefix=PREFIX_API)
app.include_router(user_router, prefix=PREFIX_API)
app.include_router(workspace_router, prefix=PREFIX_API)
app.include_router(project_router, prefix=PREFIX_API)
app.include_router(task_router, prefix=PREFIX_API)
app.include_router(label_router, prefix=PREFIX_API)
app.include_router(comment_router, prefix=PREFIX_API)

@app.get("/")
def read_root():
    return {"message": "FastAPI đang chạy!"}
