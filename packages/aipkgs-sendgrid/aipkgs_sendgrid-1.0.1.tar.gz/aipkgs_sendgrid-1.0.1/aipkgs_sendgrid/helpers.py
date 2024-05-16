import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

env_keys_exist = False
try:
    SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
    env_keys_exist = True
except Exception:
    raise Exception("add SENDGRID_API_KEY to env")


class SendgridHelpers:
    from_email = 'willnessapp@gmail.com'

    @classmethod
    def send_reset_password(cls, pin: str, to_email: str):
        return cls.send_email(from_email=cls.from_email, content=f'Use this pin code to rest your password: <strong>{pin}</strong>', to_email=to_email,
                              subject='Willness - Password Reset')

    @classmethod
    def send_validate_email(cls, pin: str, to_email: str):
        return cls.send_email(from_email=cls.from_email, content=f'Use this pin code to verify your email address: <strong>{pin}</strong>', to_email=to_email,
                              subject='Willness - Email Validation')

    @classmethod
    def send_welcome_email(cls, to_email: str):
        subject = 'Welcome to Our Service!'
        content = '<strong>Thank you for signing up. We are excited to have you with us!</strong>'
        return cls.send_email(from_email=cls.from_email, content=content, to_email=to_email, subject=subject)

    @classmethod
    def send_newsletter(cls, to_emails: list):
        subject = 'Our Monthly Newsletter'
        content = '<strong>Here is our monthly newsletter with all the latest updates and news.</strong>'
        for email in to_emails:
            cls.send_email(from_email=cls.from_email, content=content, to_email=email, subject=subject)

    @classmethod
    def send_custom_email(cls, from_email: str, content: str, to_email: str, subject: str):
        return cls.send_email(from_email=from_email, content=content, to_email=to_email, subject=subject)

    @classmethod
    def send_email(cls, from_email: str, content: str, to_email: str, subject: str) -> bool:
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content)
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
