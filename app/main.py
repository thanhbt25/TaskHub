from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import engine, Base, get_db

# 1. Lệnh này sẽ tự động tạo file database.sqlite và các bảng (nếu có)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Project")

@app.get("/")
def read_root():
    return {"message": "FastAPI đang chạy ngon lành!"}

# 2. API dùng để test kết nối database
@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Thử chạy một câu lệnh SQL đơn giản
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Kết nối SQLite thành công!"}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi kết nối: {str(e)}"}