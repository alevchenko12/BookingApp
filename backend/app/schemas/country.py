from typing import List, Annotated
from pydantic import BaseModel, StringConstraints
from schemas.city import CityRead 
# Custom string type with constraints
NameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]

# Base schema shared by multiple uses
class CountryBase(BaseModel):
    name: NameStr

# Schema for creating a country
class CountryCreate(CountryBase):
    pass

# Schema for reading a country
class CountryRead(CountryBase):
    id: int

    class Config:
        orm_mode = True

# Schema for returning a country with its cities
class CountryWithCities(CountryRead):
    cities: List[CityRead] = []
