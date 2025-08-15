"""jobtracker.emailer.email_sender

Simple SMTP email sender with attachment support.
"""
import os
import mimetypes
import smtplib
from email.message import EmailMessage
from typing import Optional

class EmailSender:
    def __init__(self, smtp_server: Optional[str] = None, smtp_port: Optional[int] = None, username: Optional[str] = None, password: Optional[str] = None):
        self.smtp_server = smtp_server or os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(smtp_port or int(os.getenv("SMTP_PORT", 587)))
        self.username = username or os.getenv("EMAIL_ADDRESS")
        self.password = password or os.getenv("EMAIL_PASSWORD")

        if not self.username or not self.password:
            raise ValueError("EMAIL_ADDRESS and EMAIL_PASSWORD must be set as environment variables or passed in")

    def send(self, to_address: str, subject: str, body: str, attachment_path: Optional[str] = None):
        msg = EmailMessage()
        msg["From"] = self.username
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.set_content(body)

        if attachment_path and os.path.exists(attachment_path):
            ctype, encoding = mimetypes.guess_type(attachment_path)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)
            with open(attachment_path, "rb") as f:
                data = f.read()
            msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=os.path.basename(attachment_path))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as s:
            s.starttls()
            s.login(self.username, self.password)
            s.send_message(msg)
