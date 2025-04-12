from enum import Enum
from datetime import date
from typing import Annotated
from pydantic import BaseModel, Field

# Enum for Payment Methods
class PaymentMethodEnum(str, Enum):
    google_pay = "Google Pay"
    card = "Card"            # Covers both credit & debit cards
    cash = "Cash"            # For pay-at-hotel or offline payments

# Base Schema (Shared Fields)
class PaymentBase(BaseModel):
    booking_id: int
    payment_date: date
    payment_method: PaymentMethodEnum
    amount: float = Field(gt=0)

# Create Schema
class PaymentCreate(PaymentBase):
    pass

# Read Schema
class PaymentRead(BaseModel):
    id: int
    payment_date: date
    payment_method: PaymentMethodEnum
    amount: float

    class Config:
        orm_mode = True
