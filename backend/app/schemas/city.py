from typing import Annotated
from pydantic import BaseModel, StringConstraints
from schemas.country import CountryRead  # optional, for nested use

# Reusable string type
NameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]

# Base schema
class CityBase(BaseModel):
    name: NameStr
    country_id: int  # link to country

# Schema for creating a city
class CityCreate(CityBase):
    pass

# Schema for reading a city (e.g. list of cities, dropdown)
class CityRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Optional: City with its country data (e.g. for admin panel or nested detail)
class CityWithCountry(CityRead):
    country: CountryRead
