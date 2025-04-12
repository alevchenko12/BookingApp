from enum import Enum
from typing import Optional, Annotated
from pydantic import BaseModel, Field, StringConstraints
from schemas.hotel import HotelRead  # Assumes you already have HotelRead schema

# Enums for Room Options
class RoomTypeEnum(str, Enum):
    single = "Single"
    double = "Double"
    suite = "Suite"

class CancellationPolicyEnum(str, Enum):
    flexible = "Flexible"
    non_refundable = "Non-refundable"

# Annotated Constraints
RoomNameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
RoomDescStr = Annotated[Optional[str], StringConstraints(strip_whitespace=True, max_length=500)]

# Base Schema (Shared Fields)
class RoomBase(BaseModel):
    name: RoomNameStr
    room_type: RoomTypeEnum
    price_per_night: float = Field(gt=0)
    capacity: int = Field(gt=0)
    description: RoomDescStr = None
    hotel_id: Optional[int] = None  # Nullable if hotel is deleted
    cancellation_policy: Optional[CancellationPolicyEnum] = None

    # Facilities — default all to False
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
    pass

# Read Schema
class RoomRead(RoomBase):
    id: int

    class Config:
        orm_mode = True

# Extended Schema (Room with Hotel)
class RoomWithHotel(RoomRead):
    hotel: Optional[HotelRead] = None
