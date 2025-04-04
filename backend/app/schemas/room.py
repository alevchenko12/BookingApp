from pydantic import BaseModel
from typing import Optional

class RoomCreate(BaseModel):
    name: str
    room_type: str
    price_per_night: float
    capacity: int
    description: Optional[str] = None
    hotel_id: int
    has_wifi: Optional[bool] = False
    allows_pets: Optional[bool] = False
    has_air_conditioning: Optional[bool] = False
    has_tv: Optional[bool] = False
    has_minibar: Optional[bool] = False
    has_balcony: Optional[bool] = False
    has_kitchen: Optional[bool] = False
    has_safe: Optional[bool] = False
    cancellation_policy: Optional[str] = None

    class Config:
        orm_mode = True
