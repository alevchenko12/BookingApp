import random
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.review import Review
from app.models.booking import Booking

# Sample review texts
sample_texts = [
    "Amazing stay!",
    "Very comfortable room.",
    "Would not recommend.",
    "Everything was clean and quiet.",
    "Perfect for a weekend getaway.",
    "Great location and friendly staff.",
    "Room was smaller than expected.",
    "Enjoyed the breakfast buffet.",
    "Nice view from the balcony.",
    None,
    ""
]

def reset_reviews(db: Session):
    deleted = db.query(Review).delete()
    db.commit()
    print(f"🗑️ Deleted {deleted} existing reviews.")

def seed_reviews(db: Session):
    added = 0
    skipped = 0
    next_id = 1  # start manually assigning IDs from 1

    completed_bookings = db.query(Booking).filter(Booking.status == "completed").all()

    for booking in completed_bookings:
        if booking.user_id is None:
            skipped += 1
            continue

        existing = db.query(Review).filter(Review.booking_id == booking.id).first()
        if existing:
            skipped += 1
            continue

        review = Review(
            id=next_id,  # manually assign ID
            user_id=booking.user_id,
            booking_id=booking.id,
            rating=random.randint(2, 5),
            text=random.choice(sample_texts)
        )

        db.add(review)
        try:
            db.commit()
            print(f"✅ Review created for booking {booking.id} (review id {next_id})")
            added += 1
            next_id += 1
        except:
            db.rollback()
            print(f"❌ Failed to insert review for booking {booking.id}")
            skipped += 1

    print(f"\n✅ {added} reviews added.")
    print(f"↩️ {skipped} skipped.")

if __name__ == "__main__":
    db: Session = SessionLocal()
    reset_reviews(db)
    seed_reviews(db)
    db.close()
