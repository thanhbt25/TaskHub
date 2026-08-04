import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


class EmailService:
    def __init__(self):
        # Trong thực tế, bạn nên lấy các thông số này từ file .env qua Pydantic BaseSettings
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.sender_email = settings.SENDER_EMAIL
        self.sender_password = settings.SENDER_PASSWORD

    def send_task_assignment_email(self, to_email: str, task_title: str, assignee_name: str):
        """Hàm gửi email (sẽ được chạy ngầm)"""
        if not to_email:
            return

        subject = f"Thông báo: Bạn vừa được giao công việc '{task_title}'"
        body = f"""
        Chào {assignee_name},

        Bạn vừa được giao xử lý công việc: "{task_title}".
        Vui lòng đăng nhập vào hệ thống TaskHub để xem chi tiết và bắt đầu thực hiện.

        Trân trọng,
        Hệ thống TaskHub
        """

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        try:
            print(f"DEBUG EMAIL: '{self.sender_email}'")
            print(f"DEBUG PASSWORD: '{self.sender_password}'")

            # Thiết lập kết nối SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Bảo mật TLS
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            print(f"Email sent successfully to {to_email}")
        except (smtplib.SMTPException, OSError) as e:
            # Ở background task, ta nên log lỗi ra console/file thay vì raise Exception
            print(f"Failed to send email to {to_email}: {e!s}")