from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from models.cancellation import Cancellation
from models.booking import Booking
from schemas.cancellation import CancellationCreate

def create_cancellation(db: Session, cancellation_in: CancellationCreate) -> Optional[Cancellation]:
    """
    Create a cancellation record for a specific booking.
    Prevents duplicate cancellations and checks that the booking exists.
    """
    # Check that booking exists
    booking = db.query(Booking).filter(Booking.id == cancellation_in.booking_id).first()
    if not booking:
        return None

    # Check if this booking already has a cancellation
    existing = db.query(Cancellation).filter(Cancellation.booking_id == cancellation_in.booking_id).first()
    if existing:
        return None

    cancellation = Cancellation(
        booking_id=cancellation_in.booking_id,
        cancellation_date=cancellation_in.cancellation_date,
        refund_amount=cancellation_in.refund_amount
    )

    db.add(cancellation)
    try:
        db.commit()
        db.refresh(cancellation)
        return cancellation
    except IntegrityError:
        db.rollback()
        return None

def get_cancellation_by_booking_id(db: Session, booking_id: int) -> Optional[Cancellation]:
    """
    Retrieve the cancellation record for a given booking.
    """
    return db.query(Cancellation).filter(Cancellation.booking_id == booking_id).first()
