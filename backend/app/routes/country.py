from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas.country import CountryCreate, CountryRead, CountryWithCities
from models.country import Country
from config.database import get_db  
from crud import country as crud_country

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("", response_model=List[CountryRead])
def list_countries(db: Session = Depends(get_db)):
    """Return all countries ordered alphabetically."""
    return crud_country.get_all_countries(db)


@router.get("/{country_id}", response_model=CountryWithCities)
def get_country_by_id(country_id: int, db: Session = Depends(get_db)):
    """Get a single country with its cities."""
    country = crud_country.get_country_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@router.post("", response_model=CountryRead, status_code=status.HTTP_201_CREATED)
def create_country(country_in: CountryCreate, db: Session = Depends(get_db)):
    """Create a new country with a unique name."""
    country = crud_country.create_country(db, country_in)
    if not country:
        raise HTTPException(status_code=400, detail="Country already exists")
    return country


@router.delete("/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_country(country_id: int, db: Session = Depends(get_db)):
    """Delete a country and all its cities."""
    deleted = crud_country.delete_country(db, country_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Country not found")


@router.get("/search/", response_model=List[CountryRead])
def search_countries(
    q: str = Query(..., min_length=1, description="Query prefix for country name"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Autocomplete search for countries by name prefix."""
    return crud_country.search_countries_by_prefix(db, query=q, limit=limit)
