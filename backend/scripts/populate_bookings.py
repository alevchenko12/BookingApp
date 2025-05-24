from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta
import random

from app.config.database import SessionLocal
from app.models.booking import Booking
from app.models.room_availability import RoomAvailability
from app.models.payment import Payment
from app.models.cancellation import Cancellation
from app.models.user import User
from app.models.room import Room
from app.models.hotel import Hotel
from app.models.city import City
from app.models.country import Country
from app.schemas.booking import BookingStatusEnum
from app.crud.room_availability import is_room_available_for_range


def reset_bookings(db: Session):
    db.query(Payment).delete()
    db.query(Cancellation).delete()
    db.query(RoomAvailability).delete()
    db.query(Booking).delete()
    db.commit()
    print("🗑️ All existing bookings, payments, cancellations, and availability deleted.")


def populate_bookings(db: Session, min_completed=15, max_total=50):
    today = date.today()
    created_total = 0
    created_completed = 0

    additional_info_options = [
        "2 adults, no special requests",
        "Family stay with 1 child",
        "Late check-in requested",
        "Anniversary weekend getaway",
        "Business trip – needs early breakfast",
        "Returning guest, prefers quiet room",
        "First-time visitor",
        "Needs airport transfer",
        "Honeymoon package",
        "Flexible checkout preferred"
    ]

    user_ids = [u.id for u in db.query(User).all()]
    if not user_ids:
        print("❌ No users available.")
        return

    france_rooms = (
        db.query(Room)
        .join(Room.hotel)
        .join(Hotel.city)
        .join(City.country)
        .filter(Country.name == "France")
        .all()
    )
    room_ids = [r.id for r in france_rooms]
    if not room_ids:
        print("❌ No rooms found in France.")
        return

    print(f"🔍 Found {len(room_ids)} French rooms. Creating bookings...")

    while created_total < max_total or created_completed < min_completed:
        room_id = random.choice(room_ids)
        user_id = random.choice(user_ids)

        check_in = today + timedelta(days=random.randint(1, 30))
        check_out = check_in + timedelta(days=random.randint(2, 5))

        if not is_room_available_for_range(db, room_id, check_in, check_out):
            continue

        if created_completed < min_completed:
            status = BookingStatusEnum.completed.value
        else:
            status = random.choice([
                BookingStatusEnum.pending.value,
                BookingStatusEnum.confirmed.value,
                BookingStatusEnum.cancelled.value,
                BookingStatusEnum.completed.value
            ])

        booking = Booking(
            user_id=user_id,
            room_id=room_id,
            booking_date=today,
            check_in_date=check_in,
            check_out_date=check_out,
            status=status,
            additional_info=random.choice(additional_info_options)
        )

        db.add(booking)
        try:
            db.commit()
            db.refresh(booking)
            created_total += 1
            if status == BookingStatusEnum.completed.value:
                created_completed += 1

            # Add room availability entries
            delta = (check_out - check_in).days
            for i in range(delta):
                block_date = check_in + timedelta(days=i)
                db.add(RoomAvailability(
                    room_id=room_id,
                    date=block_date,
                    is_available=False
                ))
            db.commit()

        except IntegrityError:
            db.rollback()

    print(f"✅ Created {created_total} bookings ({created_completed} completed).")


if __name__ == "__main__":
    db = SessionLocal()
    reset_bookings(db)
    populate_bookings(db)
    db.close()
