from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional  
from sqlalchemy import func

from models.hotel import Hotel
from models.city import City
from models.user import User

from schemas.hotel import HotelCreate, HotelUpdate


def create_hotel(db: Session, hotel_in: HotelCreate) -> Optional[Hotel]:
    """
    Create a new hotel. Ensures required fields and valid FKs.
    """
    # Optional: FK safety check
    if not db.query(City).filter(City.id == hotel_in.city_id).first():
        return None
    if not db.query(User).filter(User.id == hotel_in.owner_id).first():
        return None

    hotel = Hotel(
        name=hotel_in.name.strip(),
        address=hotel_in.address.strip(),
        description=hotel_in.description.strip() if hotel_in.description else None,
        stars=hotel_in.stars if hotel_in.stars is not None else None,
        latitude=hotel_in.latitude if hotel_in.latitude is not None else None,
        longitude=hotel_in.longitude if hotel_in.longitude is not None else None,
        city_id=hotel_in.city_id,
        owner_id=hotel_in.owner_id,
    )

    db.add(hotel)
    try:
        db.commit()
        db.refresh(hotel)
        return hotel
    except IntegrityError:
        db.rollback()
        return None


def get_hotel_by_id(db: Session, hotel_id: int) -> Optional[Hotel]:
    """
    Fetch a hotel by ID with full nested data (city, owner, rooms, photos).
    """
    return (
        db.query(Hotel)
        .options(
            joinedload(Hotel.city),
            joinedload(Hotel.owner),
            joinedload(Hotel.rooms),
            joinedload(Hotel.photos),
        )
        .filter(Hotel.id == hotel_id)
        .first()
    )


def get_all_hotels(db: Session) -> List[Hotel]:
    """
    Return all hotels, ordered alphabetically.
    """
    return db.query(Hotel).order_by(Hotel.name.asc()).all()


def update_hotel(db: Session, hotel_id: int, hotel_update: HotelUpdate) -> Optional[Hotel]:
    """
    Update a hotel with provided fields only (partial update).
    """
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        return None

    update_data = hotel_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if isinstance(value, str):
            value = value.strip()
        setattr(hotel, field, value)

    try:
        db.commit()
        db.refresh(hotel)
        return hotel
    except IntegrityError:
        db.rollback()
        return None


def delete_hotel(db: Session, hotel_id: int) -> bool:
    """
    Delete a hotel by ID. Photos will be deleted (cascade). Rooms stay.
    """
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        return False

    db.delete(hotel)
    try:
        db.commit()
        return True
    except:
        db.rollback()
        return False

def search_hotels(
    db: Session,
    country_id: Optional[int] = None,
    city_id: Optional[int] = None,
    min_stars: Optional[int] = None,
    center_lat: Optional[float] = None,
    center_lon: Optional[float] = None,
    radius_km: Optional[float] = None
) -> List[Hotel]:
    """
    Search hotels using city/country, star rating, and optional geo-radius.
    """

    query = db.query(Hotel).join(Hotel.city)

    # Filter by country (via city.country_id)
    if country_id is not None:
        query = query.filter(City.country_id == country_id)

    # Filter by city
    if city_id is not None:
        query = query.filter(Hotel.city_id == city_id)

    # Filter by star rating
    if min_stars is not None:
        query = query.filter(Hotel.stars >= min_stars)

    # Filter by radius using Haversine formula
    if center_lat is not None and center_lon is not None and radius_km is not None:
        EARTH_RADIUS_KM = 6371

        distance_expr = EARTH_RADIUS_KM * func.acos(
            func.cos(func.radians(center_lat)) *
            func.cos(func.radians(Hotel.latitude)) *
            func.cos(func.radians(Hotel.longitude) - func.radians(center_lon)) +
            func.sin(func.radians(center_lat)) *
            func.sin(func.radians(Hotel.latitude))
        )

        query = query.filter(distance_expr <= radius_km)

    return query.order_by(Hotel.name.asc()).all()
