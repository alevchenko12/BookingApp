import random
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.room import Room
from app.schemas.room import RoomTypeEnum, CancellationPolicyEnum  # Enum values

# Room type definitions
room_types = [
    (RoomTypeEnum.single.value, 1),
    (RoomTypeEnum.double.value, 2),
    (RoomTypeEnum.suite.value, 4)
]

# Sample data
descriptions = [
    "A cozy and comfortable room.",
    "Spacious and ideal for a couple.",
    "Perfect for small families.",
    "Luxurious suite with premium amenities.",
    "Modern design with a beautiful view.",
    "Comfortable space with all essentials."
]

def create_rooms(db: Session, hotel_ids=range(3, 33), rooms_per_hotel=3):
    for hotel_id in hotel_ids:
        for _ in range(rooms_per_hotel):
            room_type, capacity = random.choice(room_types)
            room = Room(
                name=f"{room_type} Room #{random.randint(100, 999)}",
                room_type=room_type,
                price_per_night=round(random.uniform(50, 300), 2),
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
    db.commit()
    print(f"✅ Rooms added for hotels 3 to 32.")

if __name__ == "__main__":
    db = SessionLocal()
    create_rooms(db)
    db.close()
