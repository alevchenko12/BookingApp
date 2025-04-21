from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.config.database import get_db
from app.schemas.room_availability import RoomAvailabilityCreate, RoomAvailabilityRead
from app.crud import room_availability as crud

router = APIRouter(
    prefix="/availability",
    tags=["Room Availability"]
)

@router.post("/", response_model=RoomAvailabilityRead, status_code=status.HTTP_201_CREATED)
def mark_unavailable(
    availability: RoomAvailabilityCreate,
    db: Session = Depends(get_db)
):
    """
    Mark a room as unavailable for a given date (e.g., due to booking).
    """
    entry = crud.create_availability_entry(db, availability)
    if not entry:
        raise HTTPException(status_code=400, detail="Room not found or already unavailable for this date.")
    return entry


@router.get("/check", response_model=bool)
def check_room_availability(
    room_id: int,
    check_in: date = Query(..., description="Start date of the period (inclusive)"),
    check_out: date = Query(..., description="End date of the period (exclusive)"),
    db: Session = Depends(get_db)
):
    """
    Check if a room is available for the entire date range.
    """
    if check_out <= check_in:
        raise HTTPException(status_code=400, detail="check_out must be after check_in")

    is_available = crud.is_room_available_for_range(db, room_id, check_in, check_out)
    return is_available


@router.get("/unavailable", response_model=List[RoomAvailabilityRead])
def get_unavailable_dates(
    room_id: int,
    check_in: date = Query(..., description="Start date of the period (inclusive)"),
    check_out: date = Query(..., description="End date of the period (exclusive)"),
    db: Session = Depends(get_db)
):
    """
    Get all unavailable dates for a room in a given range.
    """
    if check_out <= check_in:
        raise HTTPException(status_code=400, detail="check_out must be after check_in")

    return crud.get_unavailable_dates(db, room_id, check_in, check_out)
