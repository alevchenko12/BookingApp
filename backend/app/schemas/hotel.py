from typing import Annotated, Optional, TYPE_CHECKING, List
from pydantic import BaseModel, Field, StringConstraints

from schemas.city import CityRead
from schemas.user import UserRead
from schemas.hotel_photo import HotelPhotoRead  

if TYPE_CHECKING:
    from schemas.room import RoomRead  # only used for type hinting

# Reusable constraints
HotelStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]

class HotelBase(BaseModel):
    name: HotelStr
    address: HotelStr
    description: Optional[Annotated[str, StringConstraints(max_length=500)]] = None
    stars: Optional[int] = Field(default=None, ge=1, le=5)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city_id: int  # Foreign key
    owner_id: int  # Foreign key

# Used when creating a hotel
class HotelCreate(HotelBase):
    pass

# Basic read schema
class HotelRead(BaseModel):
    id: int
    name: str
    address: str
    description: Optional[str] = None
    stars: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        orm_mode = True

class HotelWithRelations(BaseModel):
    id: int
    name: str
    address: str
    description: Optional[str] = None
    stars: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    city: CityRead
    owner: UserRead
    rooms: List[RoomRead] = []
    photos: List[HotelPhotoRead] = []

    class Config:
        orm_mode = True