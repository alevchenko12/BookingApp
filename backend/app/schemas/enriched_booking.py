from pydantic import BaseModel
from typing import Optional
from app.schemas.room import CancellationPolicyEnum

class BookingUiModel(BaseModel):
    id: int
    hotel_name: str
    address: str               # From hotel
    city: str                  # From hotel.city.name
    country: str               # From hotel.city.country.name
    check_in: str              # "YYYY-MM-DD"
    check_out: str             # "YYYY-MM-DD"
    booking_date: str          # "YYYY-MM-DD"
    total_price: Optional[str] # "$123.00", or None if unpaid
    status: str
    cover_image_url: Optional[str]
    cancellation_policy: Optional[CancellationPolicyEnum]  # From room
    latitude: Optional[float]  # From hotel
    longitude: Optional[float] # From hotel

    class Config:
        orm_mode = True
