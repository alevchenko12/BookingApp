from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from datetime import date
from datetime import timedelta

from typing import List, Optional

from models.room_availability import RoomAvailability
from models.room import Room
from schemas.room_availability import RoomAvailabilityCreate

def create_availability_entry(db: Session, availability_in: RoomAvailabilityCreate) -> Optional[RoomAvailability]:
    """
    Adds an availability record marking the room as unavailable (booked) for a specific date.
    If the room is already unavailable for that date, it returns None.
    """

    # Check room existence
    if not db.query(Room).filter(Room.id == availability_in.room_id).first():
        return None

    # Check if there's already a record and the room is unavailable
    existing = db.query(RoomAvailability).filter(
        RoomAvailability.room_id == availability_in.room_id,
        RoomAvailability.date == availability_in.date
    ).first()

    if existing:
        if not existing.is_available:
            # Room already unavailable for this date
            return None
        else:
            # Overwrite availability to unavailable
            existing.is_available = False
            existing.price_override = availability_in.price_override
            try:
                db.commit()
                db.refresh(existing)
                return existing
            except IntegrityError:
                db.rollback()
                return None

    # Create new unavailability record
    availability = RoomAvailability(
        room_id=availability_in.room_id,
        date=availability_in.date,
        is_available=False,  # Explicitly set to False
        price_override=availability_in.price_override
    )

    db.add(availability)
    try:
        db.commit()
        db.refresh(availability)
        return availability
    except IntegrityError:
        db.rollback()
        return None


def is_room_available_for_range(db: Session, room_id: int, check_in: date, check_out: date) -> bool:
    """
    Return True if room has **no unavailable entries** for the date range.
    If a date is missing — it's assumed to be available.
    """
    blocked = db.query(RoomAvailability).filter(
        RoomAvailability.room_id == room_id,
        RoomAvailability.date >= check_in,
        RoomAvailability.date < check_out,
        RoomAvailability.is_available == False
    ).first()

    return blocked is None  # If no blocked dates, room is available

def get_unavailable_dates(db: Session, room_id: int, check_in: date, check_out: date) -> List[RoomAvailability]:
    """
    Return all unavailable entries (booked/blocked) in a given date range for a room.
    """
    return db.query(RoomAvailability).filter(
        RoomAvailability.room_id == room_id,
        RoomAvailability.date >= check_in,
        RoomAvailability.date < check_out,
        RoomAvailability.is_available == False
    ).all()
