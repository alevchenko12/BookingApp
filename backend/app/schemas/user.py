from typing import Annotated, TYPE_CHECKING
from pydantic import BaseModel, EmailStr, StringConstraints
from schemas.booking import BookingRead
from schemas.review import ReviewRead
from schemas.user_role import UserRoleRead

if TYPE_CHECKING:
    from schemas.hotel import HotelRead  # imported only during type checking

# Reusable types
NameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
PhoneStr = Annotated[str, StringConstraints(min_length=7, max_length=15)]
PasswordStr = Annotated[str, StringConstraints(min_length=6, max_length=100)]

# Base
class UserBase(BaseModel):
    first_name: NameStr
    last_name: NameStr
    email: EmailStr
    phone: PhoneStr | None = None

# Create
class UserCreate(UserBase):
    password: PasswordStr

# Read
class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

# Read with related info
class UserWithRelations(UserRead):
    bookings: list[BookingRead] = []
    reviews: list[ReviewRead] = []
    owned_hotels: list["HotelRead"] = [] 
    roles: list[UserRoleRead] = []

    class Config:
        orm_mode = True

UserWithRelations.model_rebuild()
