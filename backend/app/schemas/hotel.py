from __future__ import annotations  # 🔑 Enables forward references with strings (Pydantic v2)

from typing import Annotated, Optional, TYPE_CHECKING, List
from pydantic import BaseModel, Field, StringConstraints

from app.schemas.city import CityRead
from app.schemas.user import UserRead
from app.schemas.hotel_photo import HotelPhotoRead

if TYPE_CHECKING:
    from app.schemas.room import RoomRead  # Only imported for type hinting to avoid circular import

# Reusable constraints
HotelStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]

# -----------------------
# Base schema
# -----------------------
class HotelBase(BaseModel):
    name: HotelStr
    address: HotelStr
    description: Optional[Annotated[str, StringConstraints(max_length=500)]] = None
    stars: Optional[int] = Field(default=None, ge=1, le=5)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city_id: int
    owner_id: int

# -----------------------
# Create schema
# -----------------------
class HotelCreate(HotelBase):
    pass

# -----------------------
# Read schema
# -----------------------
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

# -----------------------
# Read schema with relations
# -----------------------
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
    rooms: List["RoomRead"] = []
    photos: List[HotelPhotoRead] = []

    class Config:
        orm_mode = True


# This is used for updating a hotel with only the provided fields
class HotelUpdate(BaseModel):
    name: Optional[HotelStr] = None
    address: Optional[HotelStr] = None
    description: Optional[Annotated[str, StringConstraints(max_length=500)]] = None
    stars: Optional[int] = Field(default=None, ge=1, le=5)
    latitude: Optional[float] = None
    longitude: Optional[float] = None