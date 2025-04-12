from typing import Annotated
from pydantic import BaseModel, StringConstraints
from schemas.country import CountryRead 

NameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]

# Base schema
class CityBase(BaseModel):
    name: NameStr
    country_id: int

# Create schema
class CityCreate(CityBase):
    pass

# Read schema
class CityRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Read schema with nested country
class CityWithCountry(CityRead):
    country: CountryRead
