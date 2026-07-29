from app.database import Base, engine
from fastapi import FastAPI

# 1. Lệnh này sẽ tự động tạo file database.sqlite và các bảng (nếu có)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Project")


@app.get("/")
def read_root():
    return {"message": "FastAPI đang chạy!"}
