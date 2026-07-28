import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Lấy đường dẫn tuyệt đối của thư mục chứa file database.py hiện tại (tức là thư mục 'app')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Nối thêm tên file vào cuối. Kết quả sẽ luôn chuẩn xác trên mọi máy (VD: C:\...\TaskHub\app\database.sqlite)
DB_PATH = os.path.join(BASE_DIR, "database.sqlite")

# 3. Tạo URL chuẩn của SQLite
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Tạo engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Tạo session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
Base = declarative_base()

# Dependency lấy DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()