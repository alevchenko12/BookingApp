from typing import Annotated, List, TYPE_CHECKING
from pydantic import BaseModel, StringConstraints

if TYPE_CHECKING:
    from app.schemas.city import CityRead

NameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]

class CountryBase(BaseModel):
    name: NameStr

class CountryCreate(CountryBase):
    pass

class CountryRead(CountryBase):
    id: int

    class Config:
        orm_mode = True

class CountryWithCities(CountryRead):
    cities: List["CityRead"] = []

    class Config:
        orm_mode = True

# Import after all class definitions to resolve forward reference
from app.schemas.city import CityRead
CountryWithCities.model_rebuild()
