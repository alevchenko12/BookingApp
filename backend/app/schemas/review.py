from typing import Optional, Annotated, TYPE_CHECKING
from pydantic import BaseModel, Field, StringConstraints
from app.schemas.user import UserRead

if TYPE_CHECKING:
    from app.schemas.booking import BookingRead

# Reusable constraint
ReviewText = Annotated[Optional[str], StringConstraints(strip_whitespace=True, max_length=500)]

# Base schema
class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    text: ReviewText = None

# Create schema
class ReviewCreate(ReviewBase):
    booking_id: int

# Basic read schema
class ReviewRead(ReviewBase):
    id: int

    class Config:
        orm_mode = True

# With relations
class ReviewWithRelations(ReviewRead):
    user: Optional[UserRead] = None
    booking: Optional["BookingRead"] = None

    class Config:
        orm_mode = True

# Resolve forward references
from app.schemas.booking import BookingRead
ReviewWithRelations.model_rebuild()
