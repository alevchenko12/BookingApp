from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.config.database import get_db
from app.schemas.booking import BookingCreate, BookingRead, BookingWithRelations
from app.crud.booking import (
    create_booking,
    get_booking_by_id,
    get_bookings_by_user,
    cancel_booking,
    mark_booking_as_confirmed,
    complete_and_cleanup_bookings,
    get_user_bookings_ui
)
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.enriched_booking import BookingUiModel 

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_new_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new booking using the current authenticated user.
    Automatically injects user_id from token.
    """
    # Inject current user's ID into the booking input
    booking_data = booking_in.model_copy(update={"user_id": current_user.id})
    
    booking = create_booking(db, booking_data)
    if not booking:
        raise HTTPException(status_code=400, detail="Booking could not be created")
    
    return booking

@router.get("/my-bookings")
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookings = get_bookings_by_user(db, current_user.id)

    return [
        {
            "id": booking.id,
            "booking_date": booking.booking_date,
            "check_in_date": booking.check_in_date,
            "check_out_date": booking.check_out_date,
            "status": booking.status,
            "additional_info": booking.additional_info,
            "room": booking.room,
            "payment": booking.payment,
            "cancellation": booking.cancellation,
            "reviews": booking.reviews,
        }
        for booking in bookings
    ]


@router.get("/{booking_id}", response_model=BookingWithRelations)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return {
        "id": booking.id,
        "booking_date": booking.booking_date,
        "check_in_date": booking.check_in_date,
        "check_out_date": booking.check_out_date,
        "status": booking.status,
        "additional_info": booking.additional_info,
        "room": booking.room,
        "payment": booking.payment,
        "cancellation": booking.cancellation,
        "reviews": booking.reviews,
        "user": {
            "id": booking.user.id,
            "first_name": booking.user.first_name,
            "last_name": booking.user.last_name,
            "email": booking.user.email
        } if booking.user else None
    }


# Client: cancel their own booking
@router.post("/my-bookings/{booking_id}/cancel", status_code=status.HTTP_200_OK)
def cancel_my_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = get_booking_by_id(db, booking_id)
    if not booking or booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only cancel your own bookings")

    success = cancel_booking(db, booking_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cancellation failed")

    return {"message": "Booking cancelled successfully"}


# Admin: cancel any booking by ID
@router.post("/{booking_id}/cancel", status_code=status.HTTP_200_OK)
def cancel_existing_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):
    success = cancel_booking(db, booking_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cancellation failed")
    return {"message": "Booking cancelled successfully"}


@router.post("/{booking_id}/confirm", status_code=status.HTTP_200_OK)
def confirm_existing_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):
    success = mark_booking_as_confirmed(db, booking_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot confirm booking")
    return {"message": "Booking confirmed"}


@router.post("/cleanup", status_code=status.HTTP_200_OK)
def trigger_booking_cleanup(db: Session = Depends(get_db)):
    result = complete_and_cleanup_bookings(db)
    return result

@router.get("/", response_model=List[BookingUiModel])
def get_user_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns detailed bookings (with hotel, address, city, country, image, price) for the current user.
    """
    bookings = get_user_bookings_ui(db=db, user_id=current_user.id)
    return bookings