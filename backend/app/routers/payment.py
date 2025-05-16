from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.payment import PaymentCreate, PaymentRead
from app.crud.payment import create_payment, get_payment_by_booking_id
from app.dependencies.auth import get_current_user  
from app.models.user import User
from app.crud.booking import get_booking_by_id

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)

@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_new_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):
    """
    Create a payment for a booking.
    Confirms the booking on success. Duplicate payments are prevented.
    Only the user who made the booking can pay for it.
    """
    # Check booking ownership
    booking = get_booking_by_id(db, payment_in.booking_id)
    if not booking or booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to pay for this booking.")

    # Create the payment
    payment = create_payment(db, payment_in)
    if not payment:
        raise HTTPException(
            status_code=400,
            detail="Payment could not be processed. Booking may not exist or has already been paid."
        )
    return payment


@router.get("/by-booking/{booking_id}", response_model=PaymentRead)
def get_payment_by_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Retrieve payment details for a given booking ID.
    """
    payment = get_payment_by_booking_id(db, booking_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found for this booking.")
    return payment
