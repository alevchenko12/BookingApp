from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from models.city import City
from schemas.city import CityCreate


def create_city(db: Session, city_in: CityCreate) -> Optional[City]:
    """
    Create a new city under a specific country.
    Ensures the city name is unique **within that country** (case-insensitive).
    """
    name_cleaned = city_in.name.strip()

    existing = db.query(City).filter(
        City.country_id == city_in.country_id,
        City.name.ilike(name_cleaned)
    ).first()

    if existing:
        return None  # City with that name already exists in the country

    city = City(name=name_cleaned, country_id=city_in.country_id)
    db.add(city)
    try:
        db.commit()
        db.refresh(city)
        return city
    except IntegrityError:
        db.rollback()
        return None


def get_city_by_id(db: Session, city_id: int) -> Optional[City]:
    """
    Fetch a city by its ID.
    """
    return db.query(City).filter(City.id == city_id).first()


def get_cities_by_country_id(db: Session, country_id: int) -> List[City]:
    """
    Return all cities that belong to a specific country.
    Ordered alphabetically.
    """
    return db.query(City).filter(City.country_id == country_id).order_by(City.name.asc()).all()


def delete_city(db: Session, city_id: int) -> bool:
    """
    Delete a city by ID.
    This will also delete all hotels in the city (cascading).
    """
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        return False

    db.delete(city)
    try:
        db.commit()
        return True
    except:
        db.rollback()
        return False

def search_cities_by_prefix(db: Session, query: str, country_id: Optional[int] = None, limit: int = 10) -> List[City]:
    """
    Return a list of cities that start with the given query string.
    Optionally filter by country.
    """
    if not query:
        return []

    q = db.query(City).filter(City.name.ilike(f"{query}%"))

    if country_id:
        q = q.filter(City.country_id == country_id)

    return q.order_by(City.name.asc()).limit(limit).all()
