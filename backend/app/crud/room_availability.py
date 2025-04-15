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
    Add an availability record for a room on a specific date.
    Typically used to mark it as unavailable (booked).
    """
    # FK check — ensure room exists
    if not db.query(Room).filter(Room.id == availability_in.room_id).first():
        return None

    availability = RoomAvailability(
        room_id=availability_in.room_id,
        date=availability_in.date,
        is_available=availability_in.is_available,
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
