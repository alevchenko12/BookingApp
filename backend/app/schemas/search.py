from datetime import date
from typing import List, Optional, Literal
from pydantic import BaseModel, HttpUrl
from enum import Enum

class RoomTypeEnum(str, Enum):
    single = "Single"
    double = "Double"
    suite = "Suite"

class HotelSearchRequest(BaseModel):
    destination: str
    check_in: date
    check_out: date
    rooms: int
    adults: int

    # Optional filters
    min_stars: Optional[int] = None
    has_wifi: Optional[bool] = None
    allows_pets: Optional[bool] = None
    has_kitchen: Optional[bool] = None
    has_air_conditioning: Optional[bool] = None
    has_tv: Optional[bool] = None
    has_safe: Optional[bool] = None
    has_balcony: Optional[bool] = None
    room_type: Optional[RoomTypeEnum] = None  

    # Optional sorting
    sort_by: Optional[Literal["price_asc", "price_desc", "reviews", "rating"]] = None

class HotelSearchResult(BaseModel):
    id: int
    name: str
    address: str
    city: str
    country: str
    stars: Optional[int]
    lowest_price: Optional[float]
    cover_image_url: Optional[HttpUrl]
    available_room_ids: List[int]

    # New fields for sorting/filtering
    review_count: int = 0
    average_rating: Optional[float] = None
