# from -> chọn image nền, python:3.11-slim -> phiên bản rút gọn nhẹ hơn python
# -> bát đầu từ một máy linux đã cài sẵn python:3.11 
FROM python:3.14-slim
# chọn thư mục làm việc là /app
# sau dòng này các lệnh copy, run, cmd thì đều làm việc trong app 
WORKDIR /app
# cài poetry, lệnh run để chạy lệnh trong quá trình build image 
# no-cache-dir để cài xong thì xóa cache pip để image nhỏ hơn  
RUN pip install --no-cache-dir poetry
# poetry sẽ tạo ra virtual environment, tuy nhiên docker đã là môi trường cô lập rồi, nên tắt create đi 
RUN poetry config virtualenvs.create false
# lệnh copy vào pyproject.toml và poetry.lock* vào thư mục /app
# dấu * nghĩa là nếu có thì copy, còn không thì vẫn không có lỗi 
COPY pyproject.toml poetry.lock* ./
# poetry đọc pyproject.toml rồi cài dependency
# --only main -> không cài dev-dependencies 
# --no-root -> không cài chính project thành package Python 
RUN poetry install --no-root --only main
# copy toàn bộ project 
# không copy ngay từ đầu vì còn sửa main.py ở phía trên 
COPY . .
# thông báo sử dụng cổng 8000 
EXPOSE 8000
# lệnh chạy khi container khởi động, tương đương: 
# uvicorn app.main:app --host 0.0.0.0 --port 8000
# 0.0.0.0 để bên ngoài cũng có thể truy cập được thông qua cổng 8000 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]