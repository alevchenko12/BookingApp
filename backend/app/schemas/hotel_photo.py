from pydantic import BaseModel, HttpUrl
from typing import Optional

# Shared base
class HotelPhotoBase(BaseModel):
    image_url: HttpUrl
    caption: Optional[str] = None
    is_cover: bool = False  
    hotel_id: int

# Create schema
class HotelPhotoCreate(HotelPhotoBase):
    pass

# Read schema
class HotelPhotoRead(BaseModel):
    id: int
    image_url: HttpUrl
    caption: Optional[str] = None
    is_cover: bool = False  
    class Config:
        orm_mode = True
