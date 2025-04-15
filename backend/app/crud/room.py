from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from sqlalchemy import and_

from models.room import Room
from models.hotel import Hotel
from schemas.room import RoomCreate
from schemas.room import RoomUpdate 

def create_room(db: Session, room_in: RoomCreate) -> Optional[Room]:
    """
    Create a new room in a given hotel. Ensures hotel exists before assigning.
    """
    hotel = db.query(Hotel).filter(Hotel.id == room_in.hotel_id).first()
    if not hotel:
        return None

    room = Room(
        name=room_in.name.strip(),
        room_type=room_in.room_type,
        price_per_night=room_in.price_per_night,
        capacity=room_in.capacity,
        description=room_in.description.strip() if room_in.description else None,
        cancellation_policy=room_in.cancellation_policy,
        has_wifi=room_in.has_wifi,
        allows_pets=room_in.allows_pets,
        has_air_conditioning=room_in.has_air_conditioning,
        has_tv=room_in.has_tv,
        has_minibar=room_in.has_minibar,
        has_balcony=room_in.has_balcony,
        has_kitchen=room_in.has_kitchen,
        has_safe=room_in.has_safe,
        hotel_id=room_in.hotel_id
    )

    db.add(room)
    try:
        db.commit()
        db.refresh(room)
        return room
    except IntegrityError:
        db.rollback()
        return None

def get_room_by_id(db: Session, room_id: int) -> Optional[Room]:
    """
    Fetch a room by ID, including hotel details.
    """
    return db.query(Room).options(joinedload(Room.hotel)).filter(Room.id == room_id).first()

def get_rooms_by_hotel_and_guests(db: Session, hotel_id: int, guests: int) -> List[Room]:
    """
    Return all rooms in a hotel that can accommodate at least `guests`.
    """
    return db.query(Room).filter(
        Room.hotel_id == hotel_id,
        Room.capacity >= guests
    ).order_by(Room.price_per_night.asc()).all()

def update_room(db: Session, room_id: int, room_update: RoomUpdate) -> Optional[Room]:
    """
    Partially update room fields.
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return None

    update_data = room_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if isinstance(value, str):
            value = value.strip()
        setattr(room, field, value)

    try:
        db.commit()
        db.refresh(room)
        return room
    except IntegrityError:
        db.rollback()
        return None

def delete_room(db: Session, room_id: int) -> bool:
    """
    Delete a room by ID. Will not cascade to bookings or availability.
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return False

    db.delete(room)
    try:
        db.commit()
        return True
    except:
        db.rollback()
        return False

def get_rooms_by_hotel_id(db: Session, hotel_id: int) -> List[Room]:
    """
    Return all rooms that belong to a hotel.
    """
    return db.query(Room).filter(Room.hotel_id == hotel_id).all()


def filter_rooms(
    db: Session,
    hotel_id: Optional[int] = None,
    room_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    has_wifi: Optional[bool] = None,
    allows_pets: Optional[bool] = None,
    has_air_conditioning: Optional[bool] = None,
    has_tv: Optional[bool] = None,
    has_minibar: Optional[bool] = None,
    has_balcony: Optional[bool] = None,
    has_kitchen: Optional[bool] = None,
    has_safe: Optional[bool] = None,
    min_capacity: Optional[int] = None,
) -> List[Room]:
    """
    Filter rooms with optional conditions.
    Can be scoped to a hotel or global.
    """

    query = db.query(Room)

    # Scope by hotel (if filtering inside hotel)
    if hotel_id:
        query = query.filter(Room.hotel_id == hotel_id)

    # Apply filters dynamically
    if room_type:
        query = query.filter(Room.room_type == room_type)

    if min_price is not None:
        query = query.filter(Room.price_per_night >= min_price)

    if max_price is not None:
        query = query.filter(Room.price_per_night <= max_price)

    if min_capacity is not None:
        query = query.filter(Room.capacity >= min_capacity)

    # Facility filters (only apply if passed explicitly)
    if has_wifi is not None:
        query = query.filter(Room.has_wifi == has_wifi)

    if allows_pets is not None:
        query = query.filter(Room.allows_pets == allows_pets)

    if has_air_conditioning is not None:
        query = query.filter(Room.has_air_conditioning == has_air_conditioning)

    if has_tv is not None:
        query = query.filter(Room.has_tv == has_tv)

    if has_minibar is not None:
        query = query.filter(Room.has_minibar == has_minibar)

    if has_balcony is not None:
        query = query.filter(Room.has_balcony == has_balcony)

    if has_kitchen is not None:
        query = query.filter(Room.has_kitchen == has_kitchen)

    if has_safe is not None:
        query = query.filter(Room.has_safe == has_safe)

    return query.order_by(Room.price_per_night.asc()).all()
