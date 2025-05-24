from sqlalchemy.orm import Session
from app.models.hotel import Hotel
from app.config.database import SessionLocal
import random

# Owner and city setup
owner_ids = [14, 15, 16]
city_ids = list(range(95, 182))  # City IDs

# More diverse hotel names
hotel_prefixes = [
    "Elite", "Sunset", "Golden", "Luxe", "Blue", "Maple", "Urban", "Crystal",
    "Royal", "Amber", "Vintage", "Heritage", "Skyline", "Oceanview", "Mountain",
    "Grand", "Emerald", "Serenity", "Diamond", "Majestic", "Palm", "Starry", "Velvet", "Silver"
]
hotel_suffixes = [
    "Suites", "Lodge", "Inn", "Resort", "Retreat", "Palace", "Hotel", "Stay", "Manor", "Plaza",
    "Villa", "House", "Nest", "Sanctuary", "Oasis"
]

# Expanded address parts
street_names = [
    "Maple St", "Ocean Drive", "Sunset Blvd", "Main Ave", "Park Lane",
    "Liberty Rd", "Highland Way", "Riverbank St", "King's Cross", "Central Plaza",
    "Oakwood Dr", "Willow Ave", "Broadway", "Elm St", "Pine Way", "Stone Bridge Rd"
]

# Descriptions
descriptions = [
    "A luxurious hotel with premium amenities and central location.",
    "Comfortable and affordable, ideal for solo and family travelers.",
    "Scenic views and modern interior in a quiet part of town.",
    "Newly renovated rooms with elegant design.",
    "A peaceful retreat close to tourist attractions.",
    "Elegant charm meets modern convenience.",
    "Perfect for weekend getaways and long stays alike.",
    "Experience local culture with 5-star comfort.",
    "Top-rated service with historic surroundings.",
    "Sustainable and eco-friendly hospitality."
]

def create_hotels(db: Session):
    created = 0
    for city_id in city_ids:
        used_names = set()
        for _ in range(5):  # 5 hotels per city
            # Generate a unique name per city
            while True:
                name = f"{random.choice(hotel_prefixes)} {random.choice(hotel_suffixes)}"
                if name not in used_names:
                    used_names.add(name)
                    break

            address = f"{random.randint(1, 300)} {random.choice(street_names)}"
            stars = random.randint(2, 5)  # Stars now range from 2 to 5
            latitude = round(random.uniform(45.0, 55.0), 6)
            longitude = round(random.uniform(5.0, 25.0), 6)
            description = random.choice(descriptions)
            owner_id = random.choice(owner_ids)

            hotel = Hotel(
                name=name,
                address=address,
                stars=stars,
                description=description,
                latitude=latitude,
                longitude=longitude,
                city_id=city_id,
                owner_id=owner_id
            )
            db.add(hotel)
            created += 1

    db.commit()
    print(f"✅ {created} hotels added across {len(city_ids)} cities.")

if __name__ == "__main__":
    db = SessionLocal()
    create_hotels(db)
    db.close()
