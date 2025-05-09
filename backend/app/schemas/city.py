from typing import Annotated
from pydantic import BaseModel, StringConstraints

NameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]

class CityBase(BaseModel):
    name: NameStr
    country_id: int

class CityCreate(CityBase):
    pass

class CityRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class LocationSearchResult(BaseModel):
    city_id: int
    city_name: str
    country_id: int
    country_name: str
