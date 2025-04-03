from pydantic import BaseModel, EmailStr
from typing import Optional

# Base schema for User (used for Create and Read)
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr  # Email validation
    phone: Optional[str] = None  # Optional phone number

# Schema for user creation (includes password field)
class UserCreate(UserBase):
    password: str  # Plain-text password will be hashed during creation

# Schema for User response (includes user ID and all relevant data)
class UserResponse(UserBase):
    id: int  # Including the user ID in the response model

    class Config:
        orm_mode = True  # This tells Pydantic to treat SQLAlchemy models as dicts for response
