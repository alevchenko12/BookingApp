from pydantic import BaseModel
from typing import Optional

class CityBase(BaseModel):
    name: str
    country_id: int  # Foreign key to the country

class CityCreate(CityBase):
    pass

class CityResponse(CityBase):
    id: int
    country_name: str  # To return the country name with the city

    class Config:
        orm_mode = True
