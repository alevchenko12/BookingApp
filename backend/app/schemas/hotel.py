from pydantic import BaseModel
from typing import Optional

class HotelBase(BaseModel):
    name: str
    address: str
    stars: Optional[int] = None
    description: Optional[str] = None
    city_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class HotelCreate(HotelBase):
    pass

class HotelOut(HotelBase):
    id: int

    class Config:
        orm_mode = True
