from typing import List, Annotated, TYPE_CHECKING
from pydantic import BaseModel, StringConstraints

# Prevent runtime import loop
if TYPE_CHECKING:
    from schemas.city import CityRead

NameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]

# Base schema
class CountryBase(BaseModel):
    name: NameStr

# Create schema
class CountryCreate(CountryBase):
    pass

# Read schema
class CountryRead(CountryBase):
    id: int

    class Config:
        orm_mode = True

# Read schema with cities
class CountryWithCities(CountryRead):
    cities: List["CityRead"] = []

    class Config:
        orm_mode = True

# Required to resolve forward refs in Pydantic v2
CountryWithCities.model_rebuild()
