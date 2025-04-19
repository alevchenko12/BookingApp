from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config.database import get_db  
from crud import city as crud_city
from schemas.city import CityCreate, CityRead, CityWithCountry
from models.city import City

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


@router.get("/{city_id}", response_model=CityWithCountry)
def get_city_by_id(city_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a city by its ID, including its country.
    """
    city = crud_city.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
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
