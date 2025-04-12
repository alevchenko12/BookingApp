from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

# Base Schema
class RoomAvailabilityBase(BaseModel):
    room_id: int
    date: date
    is_available: bool = False  # Default: room is not available (booked/blocked)
    price_override: Optional[float] = Field(default=None, ge=0)

# Create Schema
class RoomAvailabilityCreate(RoomAvailabilityBase):
    pass

# Read Schema
class RoomAvailabilityRead(BaseModel):
    id: int
    date: date
    is_available: bool
    price_override: Optional[float] = None

    class Config:
        orm_mode = True
