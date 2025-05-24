from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.country import Country
from app.models.city import City
from app.models.hotel import Hotel
from app.models.hotel_photo import HotelPhoto

db: Session = SessionLocal()

# Step 1: Clear hotel_photos (lowest level dependency)
db.query(HotelPhoto).delete()
db.commit()

# Step 2: Clear hotels
db.query(Hotel).delete()
db.commit()

# Step 3: Clear cities
db.query(City).delete()
db.commit()

# Step 4: Clear countries
db.query(Country).delete()
db.commit()

# Step 5: Re-insert EU + Switzerland + Ukraine
countries_to_insert = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus",
    "Czech Republic", "Denmark", "Estonia", "Finland", "France",
    "Germany", "Greece", "Hungary", "Ireland", "Italy",
    "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
    "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
    "Spain", "Sweden",
    "Switzerland", "Ukraine"
]

inserted = 0
for name in countries_to_insert:
    db.add(Country(name=name))
    inserted += 1

db.commit()
db.close()

print(f"{inserted} countries inserted (EU + Switzerland + Ukraine).")
