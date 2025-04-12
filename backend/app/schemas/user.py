from typing import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints

from schemas.booking import BookingRead
from schemas.review import ReviewRead
from schemas.hotel import HotelRead
from schemas.user_role import UserRoleRead


# Define reusable string types
NameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
PhoneStr = Annotated[str, StringConstraints(min_length=7, max_length=15)]
PasswordStr = Annotated[str, StringConstraints(min_length=6, max_length=100)]

# Shared base
class UserBase(BaseModel):
    first_name: NameStr
    last_name: NameStr
    email: EmailStr
    phone: PhoneStr | None = None

# Schema for creating a user
class UserCreate(UserBase):
    password: PasswordStr  # raw password; hashed later in logic

# Schema for reading user info
class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserWithRelations(UserRead):
    bookings: list[BookingRead] = []
    reviews: list[ReviewRead] = []
    owned_hotels: list[HotelRead] = []
    roles: list[UserRoleRead] = []
