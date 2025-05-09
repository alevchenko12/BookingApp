# app/routers/location.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.schemas.location import CityResult, CountryResult
from app.models.city import City
from app.models.country import Country

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/search", response_model=List[dict])
def search_locations(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    city_matches = db.query(City).filter(City.name.ilike(f"{q}%")).limit(5).all()
    country_matches = db.query(Country).filter(Country.name.ilike(f"{q}%")).limit(5).all()

    results = []

    for city in city_matches:
        results.append({
            "id": city.id,
            "name": city.name,
            "country_name": city.country.name if city.country else None,
            "type": "city"
        })

    for country in country_matches:
        results.append({
            "id": country.id,
            "name": country.name,
            "type": "country"
        })

    return results
