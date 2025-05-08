from pydantic_settings import BaseSettings  # Updated import for Pydantic 2.x
from typing import Optional

class Settings(BaseSettings):
    # Database config
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DATABASE_URL: str

    # JWT Token config
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Email config
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    EMAIL_FROM_NAME: Optional[str] = "Booking App"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
