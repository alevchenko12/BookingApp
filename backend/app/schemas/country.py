from pydantic import BaseModel
from typing import List

class CountryBase(BaseModel):
    name: str

class CountryCreate(CountryBase):
    pass

class CountryResponse(CountryBase):
    id: int
    cities: List[str]  # Optional: To include a list of cities

    class Config:
        orm_mode = True
