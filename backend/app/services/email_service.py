from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from app.config.settings import settings

def send_registration_email(to_email: str, user_name: str):
    subject = "Welcome to Booking App!"
    body = f"""
    <html>
        <body>
            <p>Hi <strong>{user_name}</strong>,</p>
            <p>🎉 Your account has been successfully created and verified.</p>
            <p>
                Start exploring hotels, apartments, and experiences right away in the Booking App.
            </p>
            <p>
                If you ever need help, reply to this email — we're here for you!
            </p>
            <br>
            <p>Warm wishes,<br/>The Booking App Team</p>
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.SMTP_USER}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"[Email Error] Failed to send welcome email to {to_email}: {e}")


def send_verification_email(to_email: str, token: str):
    link = f"bookingapp://verify?token={token}"  # Use your deep link
    subject = "Verify your Booking App account"
    body = f"""
    <html>
        <body>
            <p>Hi there,</p>
            <p>Please verify your email address to complete your Booking App registration.</p>
            <p>
                <a href="{link}" style="font-weight: bold; color: #2b7bb9;">Click here to verify your account</a>
            </p>
            <p>If the button doesn't work, copy and paste this link into your app:</p>
            <p><code>{link}</code></p>
            <br>
            </p>
             <p>If you didn’t create this account, you can safely ignore this email.</p>
            <br>
            <p>Thanks,<br/>The Booking App Team</p>
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.SMTP_USER}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"[Email Error] Failed to send verification email to {to_email}: {e}")
