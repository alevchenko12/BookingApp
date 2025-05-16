from typing import Annotated, Optional, TYPE_CHECKING
from pydantic import BaseModel, EmailStr, StringConstraints
from app.schemas.user_role import UserRoleRead

# Prevent circular imports at runtime
if TYPE_CHECKING:
    from app.schemas.review import ReviewRead
    from app.schemas.booking import BookingRead
    from app.schemas.hotel import HotelRead

# Reusable constraints
NameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
PhoneStr = Annotated[str, StringConstraints(min_length=7, max_length=15)]
PasswordStr = Annotated[str, StringConstraints(min_length=6, max_length=100)]

# ---------------------
# Base schema
# ---------------------
class UserBase(BaseModel):
    first_name: NameStr
    last_name: NameStr
    email: EmailStr
    phone: Optional[PhoneStr] = None


# ---------------------
# Create schema
# ---------------------
class UserCreate(UserBase):
    password: PasswordStr


# ---------------------
# Read schema
# ---------------------
class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------
# Read with related entities
# ---------------------
class UserWithRelations(UserRead):
    bookings: list["BookingRead"] = []
    reviews: list["ReviewRead"] = []
    owned_hotels: list["HotelRead"] = []
    roles: list[UserRoleRead] = []

    class Config:
        orm_mode = True


# ---------------------
# Update schema
# ---------------------
class UserUpdate(BaseModel):
    first_name: Optional[NameStr] = None
    last_name: Optional[NameStr] = None
    phone: Optional[PhoneStr] = None

# ---------------------
# Forgot Password Flow Schemas
# ---------------------

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str


# ---------------------
# Resolve forward references
# ---------------------
from app.schemas.booking import BookingRead
from app.schemas.review import ReviewRead
from app.schemas.hotel import HotelRead

UserWithRelations.model_rebuild()
