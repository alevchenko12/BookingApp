from __future__ import annotations

from enum import Enum
from typing import Optional, Annotated, TYPE_CHECKING
from pydantic import BaseModel, Field, StringConstraints

if TYPE_CHECKING:
    pass  # Removed HotelRead to break circular import

# -----------------------
# ENUMS
# -----------------------
class RoomTypeEnum(str, Enum):
    single = "Single"
    double = "Double"
    suite = "Suite"

class CancellationPolicyEnum(str, Enum):
    flexible = "Flexible"
    non_refundable = "Non-refundable"

# -----------------------
# Shared annotated types
# -----------------------
RoomNameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
RoomDescStr = Annotated[Optional[str], StringConstraints(strip_whitespace=True, max_length=500)]

# -----------------------
# Base schema
# -----------------------
class RoomBase(BaseModel):
    name: RoomNameStr
    room_type: RoomTypeEnum
    price_per_night: float = Field(gt=0)
    capacity: int = Field(gt=0)
    description: RoomDescStr = None
    cancellation_policy: Optional[CancellationPolicyEnum] = None
    has_wifi: bool = False
    allows_pets: bool = False
    has_air_conditioning: bool = False
    has_tv: bool = False
    has_minibar: bool = False
    has_balcony: bool = False
    has_kitchen: bool = False
    has_safe: bool = False

# -----------------------
# Create schema
# -----------------------
class RoomCreate(RoomBase):
    hotel_id: int

# -----------------------
# Read schema
# -----------------------
class RoomRead(RoomBase):
    id: int
    hotel_id: Optional[int] = None

    class Config:
        orm_mode = True

# -----------------------
# Update schema
# -----------------------
class RoomUpdate(BaseModel):
    name: Optional[RoomNameStr] = None
    room_type: Optional[RoomTypeEnum] = None
    price_per_night: Optional[float] = Field(gt=0, default=None)
    capacity: Optional[int] = Field(gt=0, default=None)
    description: RoomDescStr = None
    cancellation_policy: Optional[CancellationPolicyEnum] = None
    has_wifi: Optional[bool] = None
    allows_pets: Optional[bool] = None
    has_air_conditioning: Optional[bool] = None
    has_tv: Optional[bool] = None
    has_minibar: Optional[bool] = None
    has_balcony: Optional[bool] = None
    has_kitchen: Optional[bool] = None
    has_safe: Optional[bool] = None
