from datetime import date
from enum import Enum
from typing import Optional, Annotated

from pydantic import BaseModel, StringConstraints
from schemas.user import UserRead
from schemas.room import RoomRead
from schemas.payment import PaymentRead
from schemas.cancellation import CancellationRead
from schemas.review import ReviewRead

# Enum for booking status
class BookingStatusEnum(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

# String constraints
BookingInfoStr = Annotated[Optional[str], StringConstraints(strip_whitespace=True, max_length=500)]

# Base Schema
class BookingBase(BaseModel):
    booking_date: date
    check_in_date: date
    check_out_date: date
    status: BookingStatusEnum = BookingStatusEnum.pending
    additional_info: BookingInfoStr = None

# Create Schema
class BookingCreate(BookingBase):
    user_id: int  # Required when creating
    room_id: int  # Required when creating

# Read Schema
class BookingRead(BookingBase):
    id: int

    class Config:
        orm_mode = True

# Read Schema with Relations
class BookingWithRelations(BookingRead):
    user: Optional[UserRead] = None
    room: Optional[RoomRead] = None
    payment: Optional[PaymentRead] = None
    cancellation: Optional[CancellationRead] = None
    reviews: list[ReviewRead] = []
