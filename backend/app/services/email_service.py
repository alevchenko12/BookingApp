from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from app.config.settings import settings

def send_registration_email(to_email: str, user_name: str):
    subject = "Welcome to Booking App"
    body = f"""
    Hi {user_name},

    Thank you for registering with Booking App!

    We're excited to have you on board. If you have any questions, feel free to reach out.

    Happy booking!
    — The Booking App Team
    """

    msg = MIMEMultipart()
    msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.SMTP_USER}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"[Email Error] Failed to send welcome email to {to_email}: {e}")

def send_verification_email(to_email: str, token: str):
    link = f"bookingapp://verify?token={token}"
    subject = "Verify your Booking App account"
    body = f"""
    Hi,

    Please verify your email address to complete your Booking App registration.

    Click the link below to verify:
    {link}

    If you did not initiate this request, please ignore this email.

    Thanks,
    The Booking App Team
    """

    msg = MIMEMultipart()
    msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.SMTP_USER}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"[Email Error] Failed to send verification email to {to_email}: {e}")
