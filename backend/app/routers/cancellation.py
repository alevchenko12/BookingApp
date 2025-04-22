from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.cancellation import CancellationCreate, CancellationRead
from app.crud.cancellation import create_cancellation, get_cancellation_by_booking_id

router = APIRouter(
    prefix="/cancellations",
    tags=["Cancellations"],
)


@router.post("/", response_model=CancellationRead, status_code=status.HTTP_201_CREATED)
def create_new_cancellation(cancellation_in: CancellationCreate, db: Session = Depends(get_db)):
    """
    Create a cancellation record for a booking.
    Admin-level endpoint — does not check user ownership.
    """
    cancellation = create_cancellation(db, cancellation_in)
    if not cancellation:
        raise HTTPException(
            status_code=400,
            detail="Cancellation could not be created — booking may not exist or already cancelled."
        )
    return cancellation


@router.get("/by-booking/{booking_id}", response_model=CancellationRead)
def get_cancellation_by_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the cancellation record for a given booking ID.
    """
    cancellation = get_cancellation_by_booking_id(db, booking_id)
    if not cancellation:
        raise HTTPException(status_code=404, detail="Cancellation not found for this booking")
    return cancellation
