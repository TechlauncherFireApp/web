import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from services.secrets import SecretService

secret = SecretService(f"email/{os.environ.get('env', 'dev')}/smtp")


class MailSender:
    smtp_endpoint = None
    user_name = None
    password = None
    from_email = None

    def __init__(self):
        secret_dict = secret.get()
        self.smtp_endpoint = secret_dict['smtp_endpoint']
        self.user_name = secret_dict['user_name']
        self.password = secret_dict['password']
        self.from_email = secret_dict['from_email']

    def email(self, receiver, subject, content, sender=None):
        # sms mail service
        if not sender:
            sender = self.from_email
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')

        server = smtplib.SMTP(self.smtp_endpoint, 587)
        server.starttls()
        server.login(self.user_name, self.password)
        server.sendmail(sender, receiver, message.as_string())
        print("Send mail successfully")
