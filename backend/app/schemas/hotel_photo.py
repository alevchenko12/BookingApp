from pydantic import BaseModel, HttpUrl
from typing import Annotated, Optional
from pydantic import StringConstraints

# Optional: reusables
CaptionStr = Annotated[str, StringConstraints(strip_whitespace=True, max_length=255)]
CoverFlag = Annotated[str, StringConstraints(strip_whitespace=True, max_length=10)]

# Shared base (not strictly necessary but helpful for reuse if needed)
class HotelPhotoBase(BaseModel):
    image_url: HttpUrl
    caption: Optional[CaptionStr] = None
    is_cover: Optional[CoverFlag] = None
    hotel_id: int  # passed when uploading/creating

# Schema for creating a new photo (used after image is uploaded)
class HotelPhotoCreate(HotelPhotoBase):
    pass

# Schema for reading photo info (e.g., inside HotelWithRelations)
class HotelPhotoRead(BaseModel):
    id: int
    image_url: HttpUrl
    caption: Optional[str] = None
    is_cover: Optional[str] = None

    class Config:
        orm_mode = True
