# app/schemas/location.py

from pydantic import BaseModel
from typing import Optional

class CountryResult(BaseModel):
    id: int
    name: str
    type: str = "country"

class CityResult(BaseModel):
    id: int
    name: str
    country_name: Optional[str]
    type: str = "city"
