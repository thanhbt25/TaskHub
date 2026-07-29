from app.database import Base, engine
from fastapi import FastAPI
from app.api.auth import router as auth_router 

PREFIX_API = "/api/v1"
# 1. Lệnh này sẽ tự động tạo file database.sqlite và các bảng (nếu có)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskHub API",
    description="Hệ thống quản lý công việc TaskHub API",
    version="1.0.0"
)

# Include router 
app.include_router(auth_router, prefix=PREFIX_API)

@app.get("/")
def read_root():
    return {"message": "FastAPI đang chạy!"}
