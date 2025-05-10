from datetime import date
from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class HotelSearchRequest(BaseModel):
    destination: str
    check_in: date
    check_out: date
    rooms: int
    adults: int

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
