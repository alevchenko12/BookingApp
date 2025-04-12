from enum import Enum
from typing import Optional, Annotated
from pydantic import BaseModel, Field, StringConstraints
from schemas.hotel import HotelRead  # Assuming you already have this

# Enum for Room Type
class RoomTypeEnum(str, Enum):
    single = "Single"
    double = "Double"
    suite = "Suite"

# Enum for Cancellation Policy
class CancellationPolicyEnum(str, Enum):
    flexible = "Flexible"
    non_refundable = "Non-refundable"

# Annotated string constraints
RoomNameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
RoomDescStr = Annotated[Optional[str], StringConstraints(strip_whitespace=True, max_length=500)]

# Base Schema (Shared Fields)
class RoomBase(BaseModel):
    name: RoomNameStr
    room_type: RoomTypeEnum
    price_per_night: float = Field(gt=0)
    capacity: int = Field(gt=0)
    description: RoomDescStr = None
    cancellation_policy: Optional[CancellationPolicyEnum] = None

    # Facilities — all default to False
    has_wifi: bool = False
    allows_pets: bool = False
    has_air_conditioning: bool = False
    has_tv: bool = False
    has_minibar: bool = False
    has_balcony: bool = False
    has_kitchen: bool = False
    has_safe: bool = False

# Create Schema
class RoomCreate(RoomBase):
    hotel_id: int  # Required when creating a room

# Read Schema
class RoomRead(RoomBase):
    id: int
    hotel_id: Optional[int] = None  # Nullable if hotel was deleted

    class Config:
        orm_mode = True

# Extended Schema (Room with Hotel)
class RoomWithHotel(RoomRead):
    hotel: Optional[HotelRead] = None