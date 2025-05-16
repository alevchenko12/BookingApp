from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional

from app.models.payment import Payment
from app.models.booking import Booking
from app.schemas.payment import PaymentCreate
from app.crud.booking import mark_booking_as_confirmed


def create_payment(db: Session, payment_in: PaymentCreate) -> Optional[Payment]:
    """
    Create a payment for a booking and mark the booking as confirmed.
    Prevents duplicate payments.
    """

    # 1. Ensure booking exists
    booking = db.query(Booking).filter(Booking.id == payment_in.booking_id).first()
    if not booking:
        return None

    # 2. Prevent duplicate payment for this booking
    existing = db.query(Payment).filter(Payment.booking_id == payment_in.booking_id).first()
    if existing:
        return None

    # 3. Create payment
    payment = Payment(
        booking_id=payment_in.booking_id,
        payment_date=payment_in.payment_date,
        payment_method=payment_in.payment_method.value,
        amount=payment_in.amount
    )

    db.add(payment)
    try:
        db.commit()
        db.refresh(payment)
    except IntegrityError:
        db.rollback()
        return None

    # 4. Mark booking as confirmed (if pending)
    mark_booking_as_confirmed(db, booking.id)

    return payment


def get_payment_by_booking_id(db: Session, booking_id: int) -> Optional[Payment]:
    """
    Retrieve the payment for a given booking.
    """
    return db.query(Payment).filter(Payment.booking_id == booking_id).first()
