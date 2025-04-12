from datetime import date
from pydantic import BaseModel, Field

# Base Schema (Shared Fields)
class CancellationBase(BaseModel):
    booking_id: int
    cancellation_date: date
    refund_amount: float = Field(ge=0)  # Refund must be >= 0

# Create Schema
class CancellationCreate(CancellationBase):
    pass

# Read Schema
class CancellationRead(BaseModel):
    id: int
    cancellation_date: date
    refund_amount: float

    class Config:
        orm_mode = True
