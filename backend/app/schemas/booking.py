from datetime import date
from enum import Enum
from typing import Optional, Annotated, TYPE_CHECKING

from pydantic import BaseModel, Field, StringConstraints
from app.schemas.user import UserRead
from app.schemas.room import RoomRead
from app.schemas.payment import PaymentRead
from app.schemas.cancellation import CancellationRead

if TYPE_CHECKING:
    from app.schemas.review import ReviewRead

class BookingStatusEnum(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

BookingInfoStr = Annotated[Optional[str], StringConstraints(strip_whitespace=True, max_length=500)]

class BookingBase(BaseModel):
    booking_date: date
    check_in_date: date
    check_out_date: date
    status: BookingStatusEnum = BookingStatusEnum.pending
    additional_info: BookingInfoStr = None

class BookingCreate(BookingBase):
    room_id: int

class BookingRead(BookingBase):
    id: int

    class Config:
        orm_mode = True

class BookingWithRelations(BookingRead):
    user: Optional[UserRead] = None
    room: Optional[RoomRead] = None
    payment: Optional[PaymentRead] = None
    cancellation: Optional[CancellationRead] = None
    reviews: list["ReviewRead"] = []

    class Config:
        orm_mode = True

from app.schemas.review import ReviewRead
BookingWithRelations.model_rebuild()
