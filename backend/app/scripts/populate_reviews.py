import random
from sqlalchemy.orm import Session
from datetime import datetime
from app.config.database import SessionLocal
from app.models.review import Review
from app.models.booking import Booking
from app.models.user import User
from app.schemas.review import ReviewCreate
from app.crud.review import create_review

# Sample texts to pick from
sample_texts = [
    "Amazing stay!", "Very comfortable room.", "Would not recommend.",
    "Everything was clean and quiet.", "Perfect for a weekend getaway.",
    None, "", "Staff was helpful and polite."
]

# Bookings to populate reviews for
BOOKING_IDS = list(range(1, 18))
USER_IDS = [1, 2, 3, 7]

def seed_reviews():
    db: Session = SessionLocal()

    try:
        for booking_id in BOOKING_IDS:
            booking = db.query(Booking).filter(Booking.id == booking_id).first()
            if not booking:
                print(f"Booking {booking_id} not found.")
                continue

            if booking.status != "completed":
                print(f"Skipping booking {booking_id} (status: {booking.status})")
                continue

            if db.query(Review).filter(Review.booking_id == booking_id).first():
                print(f"Booking {booking_id} already has a review.")
                continue

            user_id = booking.user_id or random.choice(USER_IDS)

            review_data = ReviewCreate(
                rating=random.randint(1, 5),
                text=random.choice(sample_texts),
                user_id=user_id,
                booking_id=booking_id
            )

            review = create_review(db, review_data)
            if review:
                print(f"✅ Created review for booking {booking_id}")
            else:
                print(f"❌ Failed to create review for booking {booking_id}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_reviews()
