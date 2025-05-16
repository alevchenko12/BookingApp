from sqlalchemy.orm import Session
from app.models.hotel import Hotel
from app.config.database import SessionLocal
import random

# Sample data
hotel_names = [
    "Grand Palace Hotel", "Royal Stay", "Comfort Inn", "Urban Retreat", "Heritage Lodge",
    "Skyline Suites", "Oceanview Resort", "Mountain Escape", "Historic Haven", "Boutique Bliss"
]

addresses = [
    "Main St 123", "Sunset Blvd 45", "Ocean Ave 78", "Park Lane 32", "Victory Sq 5",
    "Highland Rd 67", "Maple Street 90", "King’s Cross 12", "Central Ave 9", "Liberty St 3"
]

descriptions = [
    "A beautiful place with modern amenities.",
    "Located in the heart of the city, close to attractions.",
    "Great for families and solo travelers alike.",
    "Charming decor and peaceful surroundings.",
    "Ideal for business trips or relaxing getaways."
]

# You already have 25 city IDs and 4 user IDs from your database
city_ids = [4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
owner_ids = [1, 2, 3, 7]

def create_sample_hotels(db: Session, count: int = 30):
    for i in range(count):
        hotel = Hotel(
            name=random.choice(hotel_names) + f" #{i+1}",
            address=random.choice(addresses),
            stars=random.randint(3, 5),
            description=random.choice(descriptions),
            city_id=random.choice(city_ids),
            latitude=round(random.uniform(45.0, 52.0), 6),
            longitude=round(random.uniform(5.0, 25.0), 6),
            owner_id=random.choice(owner_ids)
        )
        db.add(hotel)
    db.commit()
    print(f"{count} hotels added.")

if __name__ == "__main__":
    db = SessionLocal()
    create_sample_hotels(db)
    db.close()
