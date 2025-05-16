from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from enum import Enum


# --- Room fields ---
class RoomTypeEnum(str, Enum):
    single = "Single"
    double = "Double"
    suite = "Suite"

class CancellationPolicyEnum(str, Enum):
    flexible = "Flexible"
    non_refundable = "Non-refundable"

class RoomDetail(BaseModel):
    id: int
    name: str
    room_type: RoomTypeEnum
    price_per_night: float
    capacity: int
    description: Optional[str]
    cancellation_policy: Optional[CancellationPolicyEnum]

    has_wifi: bool
    allows_pets: bool
    has_air_conditioning: bool
    has_tv: bool
    has_minibar: bool
    has_balcony: bool
    has_kitchen: bool
    has_safe: bool

    class Config:
        orm_mode = True


# --- Review fields ---
class ReviewDetail(BaseModel):
    id: int
    rating: int
    text: Optional[str]
    user_name: Optional[str]  # from related User
    class Config:
        orm_mode = True


# --- Final hotel detail response ---
class HotelDetailResponse(BaseModel):
    id: int
    name: str
    address: str
    description: Optional[str]
    stars: Optional[int]
    city: str
    country: str

    latitude: Optional[float]
    longitude: Optional[float]

    photos: List[HttpUrl]
    rooms: List[RoomDetail]
    reviews: List[ReviewDetail]

    class Config:
        orm_mode = True
