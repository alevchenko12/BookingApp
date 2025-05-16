from __future__ import annotations
from typing import Annotated, Optional, TYPE_CHECKING, List
from pydantic import BaseModel, Field, StringConstraints

from app.schemas.city import CityRead
from app.schemas.hotel_photo import HotelPhotoRead

if TYPE_CHECKING:
    from app.schemas.room import RoomRead

HotelStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]

class HotelBase(BaseModel):
    name: HotelStr
    address: HotelStr
    description: Optional[Annotated[str, StringConstraints(max_length=500)]] = None
    stars: Optional[int] = Field(default=None, ge=1, le=5)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city_id: int
    owner_id: int

class HotelCreate(HotelBase):
    pass

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
    rooms: List["RoomRead"] = []
    photos: List[HotelPhotoRead] = []

    class Config:
        orm_mode = True

class HotelUpdate(BaseModel):
    name: Optional[HotelStr] = None
    address: Optional[HotelStr] = None
    description: Optional[Annotated[str, StringConstraints(max_length=500)]] = None
    stars: Optional[int] = Field(default=None, ge=1, le=5)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

from app.schemas.room import RoomRead
HotelWithRelations.model_rebuild()
