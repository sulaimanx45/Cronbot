import smtplib


class EmailSender:
    def __init__(self, username: str, password: str, smtp_server: str="smtp.gmail.com", smtp_port: int=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, to_email: str, subject: str, body: str):
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(self.username, to_email, message)