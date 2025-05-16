from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.config.database import get_db  
from app.crud import city as crud_city
from app.schemas.city import CityCreate, CityRead
from app.models.city import City


router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=CityRead, status_code=status.HTTP_201_CREATED)
def create_city(city_in: CityCreate, db: Session = Depends(get_db)):
    """
    Create a new city under a specific country. City names must be unique within the country.
    """
    city = crud_city.create_city(db, city_in)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City already exists in this country or invalid country ID.",
        )
    return city


@router.get("/by_country/{country_id}", response_model=List[CityRead])
def get_cities_by_country(country_id: int, db: Session = Depends(get_db)):
    """
    List all cities that belong to a specific country.
    """
    return crud_city.get_cities_by_country_id(db, country_id)


@router.get("/search", response_model=List[CityRead])
def search_cities(
    q: str = Query(..., min_length=1),
    country_id: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Autocomplete search for cities by name prefix.
    Optional: restrict to a specific country.
    """
    return crud_city.search_cities_by_prefix(db, query=q, country_id=country_id, limit=limit)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    """
    Delete a city by ID. Also deletes all associated hotels (via cascade).
    """
    success = crud_city.delete_city(db, city_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")


@router.get("/{city_id}")
def get_city_with_country(city_id: int, db: Session = Depends(get_db)):
    """
    Get city with its country's name only (avoids circular import).
    """
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return {
        "id": city.id,
        "name": city.name,
        "country": {
            "name": city.country.name
        } if city.country else None
    }

from app.schemas.city import LocationSearchResult

@router.get("/location-autocomplete", response_model=List[LocationSearchResult])
def location_autocomplete(
    q: str = Query(..., min_length=1),
    limit: int = 10,
    db: Session = Depends(get_db),
):
    cities = crud_city.search_city_with_country(db, query=q, limit=limit)
    return [
        LocationSearchResult(
            city_id=city.id,
            city_name=city.name,
            country_id=city.country.id,
            country_name=city.country.name,
        )
        for city in cities if city.country
    ]
