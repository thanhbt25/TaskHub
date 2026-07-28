import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.sqlite")

DATABASE_URL = f"sqlite:///{DB_PATH}"

# Tạo engine: tạo 1 đối tượng quản lý kết nối DB, khi tương tác với DB đều phải qua cái này 
# SQLite chỉ cho phép 1 thread kết nối, FastAPI thì nhiều
# sử dụng connect_args={"check_same_thread": False} để SQLite cho phép nhều thread dùng 
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Tạo phiên làm việc với DB
# Engine chỉ biết DB ở đâu, còn session là nơi thực hiện câu lệnh 
# sesionmake là hàm tạo session 
# bind=engine -> sử dụng engine nào 
# autocommit=False -> khi db.add(...) thì SQLAlchemy không tự lưu mà phải db.commt thì mới ghi xuống db
# autoflush=False -> chặn việc tự động đồng bộ dữ liệu xuống DB trước khi chạy truy vấn 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model: là lớp cha của tất cả model 
# bất cứ 1 class nào kế thừa Base tức là đó là 1 bảng trong db 
Base = declarative_base()

# Dependency lấy DB session
# nhiệm vụ: tạo session, đưa session cho api sử dụng và tự động đóng session khi kết thúc 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()