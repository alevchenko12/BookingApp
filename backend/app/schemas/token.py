from pydantic import BaseModel
from app.schemas.user import UserRead

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenWithUser(Token):
    user: UserRead

from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str
