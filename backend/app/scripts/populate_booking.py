from datetime import date, timedelta
import random
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.booking import Booking
from app.models.room_availability import RoomAvailability
from app.crud.room_availability import is_room_available_for_range
from sqlalchemy.exc import IntegrityError

db: Session = SessionLocal()

room_ids = [1, 2] + list(range(7, 97))
user_ids = [1, 2, 3, 7]
today = date.today()
created = 0

for _ in range(15):
    room_id = random.choice(room_ids)
    user_id = random.choice(user_ids)
    check_in = today + timedelta(days=random.randint(1, 20))
    check_out = check_in + timedelta(days=random.randint(2, 4))

    if not is_room_available_for_range(db, room_id, check_in, check_out):
        continue

    booking = Booking(
        user_id=user_id,
        room_id=room_id,
        booking_date=today,
        check_in_date=check_in,
        check_out_date=check_out,
        status="completed",
        additional_info="Sample booking"
    )

    try:
        db.add(booking)
        db.commit()
        db.refresh(booking)

        for i in range((check_out - check_in).days):
            block_date = check_in + timedelta(days=i)
            availability = RoomAvailability(
                room_id=room_id,
                date=block_date,
                is_available=False
            )
            db.add(availability)
        db.commit()
        created += 1
    except IntegrityError:
        db.rollback()

db.close()
print(f"{created} bookings inserted.")
