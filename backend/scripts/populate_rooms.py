import random
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.room import Room
from app.models.hotel import Hotel
from app.schemas.room import RoomTypeEnum, CancellationPolicyEnum

# Realistic room name patterns
room_adjectives = [
    "Deluxe", "Executive", "Standard", "Superior", "Premium", "Cozy",
    "Modern", "Elegant", "Spacious", "Classic", "Oceanview", "Mountain View"
]
room_bed_types = [
    "King", "Queen", "Double", "Single", "Twin", "Studio", "Suite"
]

# Room types: (type, capacity)
room_types = [
    (RoomTypeEnum.single.value, 1),
    (RoomTypeEnum.double.value, 2),
    (RoomTypeEnum.suite.value, 4)
]

descriptions = [
    "A cozy and comfortable room for a restful stay.",
    "Spacious and ideal for couples or business travelers.",
    "Perfect for families or small groups with elegant touches.",
    "Top-tier suite with premium amenities and great views.",
    "Smartly designed room offering a blend of luxury and practicality.",
    "Bright space with stylish interiors and high-end finishes."
]

def create_rooms(db: Session):
    # Step 1: Delete all existing rooms
    deleted = db.query(Room).delete()
    db.commit()
    print(f"🗑️ Deleted {deleted} existing rooms.")

    # Step 2: Generate new rooms per hotel
    hotel_ids = [h.id for h in db.query(Hotel).all()]
    total_rooms = 0

    for hotel_id in hotel_ids:
        num_rooms = random.randint(2, 4)
        for _ in range(num_rooms):
            room_type, capacity = random.choice(room_types)
            name = f"{random.choice(room_adjectives)} {random.choice(room_bed_types)} Room"
            room = Room(
                name=name,
                room_type=room_type,
                price_per_night=round(random.uniform(60, 300), 2),
                capacity=capacity,
                description=random.choice(descriptions),
                hotel_id=hotel_id,
                has_wifi=random.choice([True, False]),
                allows_pets=random.choice([True, False]),
                has_air_conditioning=random.choice([True, False]),
                has_tv=random.choice([True, False]),
                has_minibar=random.choice([True, False]),
                has_balcony=random.choice([True, False]),
                has_kitchen=random.choice([True, False]),
                has_safe=random.choice([True, False]),
                cancellation_policy=random.choice([
                    CancellationPolicyEnum.flexible.value,
                    CancellationPolicyEnum.non_refundable.value
                ])
            )
            db.add(room)
            total_rooms += 1

    db.commit()
    print(f"✅ {total_rooms} rooms inserted across {len(hotel_ids)} hotels.")

# Entry point
if __name__ == "__main__":
    db = SessionLocal()
    create_rooms(db)
    db.close()
