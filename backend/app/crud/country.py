from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from models.country import Country
from schemas.country import CountryCreate
from typing import List, Optional


def create_country(db: Session, country_in: CountryCreate) -> Optional[Country]:
    """
    Create a new country with a unique name.
    Returns the created country or None if it already exists.
    """
    name_cleaned = country_in.name.strip()
    
    existing = db.query(Country).filter(Country.name.ilike(name_cleaned)).first()
    if existing:
        return None  # Country already exists (case-insensitive)

    country = Country(name=name_cleaned)
    db.add(country)
    try:
        db.commit()
        db.refresh(country)
        return country
    except IntegrityError:
        db.rollback()
        return None


def get_country_by_id(db: Session, country_id: int) -> Optional[Country]:
    """
    Fetch a country by ID.
    Includes its related cities via joinedload().
    """
    return (
        db.query(Country)
        .options(joinedload(Country.cities))  # eager-load cities
        .filter(Country.id == country_id)
        .first()
    )


def get_all_countries(db: Session) -> List[Country]:
    """
    Return all countries.
    """
    return db.query(Country).order_by(Country.name.asc()).all()


def delete_country(db: Session, country_id: int) -> bool:
    """
    Delete a country by ID.
    Cascades to delete all related cities.
    Returns True if deleted, False if not found.
    """
    country = db.query(Country).filter(Country.id == country_id).first()
    if not country:
        return False

    db.delete(country)
    try:
        db.commit()
        return True
    except:
        db.rollback()
        return False

def search_countries_by_prefix(db: Session, query: str, limit: int = 10) -> List[Country]:
    """
    Return a list of countries whose names start with the given query string.
    Useful for autocomplete suggestions.
    """
    if not query:
        return []

    return (
        db.query(Country)
        .filter(Country.name.ilike(f"{query}%"))
        .order_by(Country.name.asc())
        .limit(limit)
        .all()
    )
