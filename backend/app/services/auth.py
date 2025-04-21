# services/auth_service.py

from datetime import datetime, timedelta
from datetime import datetime, timezone
from typing import Optional
from jose import jwt

from app.config.jwt_config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a JWT token from user data (e.g., email).
    """
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
