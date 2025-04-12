from typing import Optional, Annotated
from pydantic import BaseModel, Field, StringConstraints
from schemas.user import UserRead
from schemas.booking import BookingRead

# Reusable Constraints
ReviewText = Annotated[Optional[str], StringConstraints(strip_whitespace=True, max_length=500)]

# Base Schema (Shared Fields)
class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    text: ReviewText = None

# Create Schema
class ReviewCreate(ReviewBase):
    user_id: int
    booking_id: int

# Read Schema
class ReviewRead(BaseModel):
    id: int
    rating: int
    text: Optional[str] = None

    class Config:
        orm_mode = True

# Extended Schema (with relations)
class ReviewWithRelations(ReviewRead):
    user: Optional[UserRead] = None
    booking: Optional[BookingRead] = None
