from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List

from models.review import Review
from models.user import User
from models.booking import Booking
from models.room import Room
from schemas.review import ReviewCreate

def create_review(db: Session, review_in: ReviewCreate) -> Optional[Review]:
    """
    Create a review for a completed booking by the user who made it.
    Prevents duplicate reviews.
    """
    # Validate user
    user = db.query(User).filter(User.id == review_in.user_id).first()
    if not user:
        return None

    # Validate booking exists and belongs to user and is completed
    booking = db.query(Booking).filter(Booking.id == review_in.booking_id).first()
    if not booking or booking.user_id != review_in.user_id or booking.status != "completed":
        return None

    # Prevent duplicate review
    existing = db.query(Review).filter(Review.booking_id == review_in.booking_id).first()
    if existing:
        return None

    # Create review
    review = Review(
        rating=review_in.rating,
        text=review_in.text.strip() if review_in.text else None,
        user_id=review_in.user_id,
        booking_id=review_in.booking_id,
    )

    db.add(review)
    try:
        db.commit()
        db.refresh(review)
        return review
    except IntegrityError:
        db.rollback()
        return None

def get_review_by_id(db: Session, review_id: int) -> Optional[Review]:
    """
    Fetch a review by its ID.
    """
    return db.query(Review).filter(Review.id == review_id).first()


def get_reviews_by_user(db: Session, user_id: int) -> List[Review]:
    """
    Return all reviews submitted by a specific user.
    """
    return db.query(Review).filter(Review.user_id == user_id).all()


def get_reviews_by_booking(db: Session, booking_id: int) -> List[Review]:
    """
    Return reviews attached to a specific booking.
    Normally only 1 per booking.
    """
    return db.query(Review).filter(Review.booking_id == booking_id).all()


def get_reviews_for_hotel(
    db: Session,
    hotel_id: int,
    min_rating: Optional[int] = None,
    only_with_text: bool = False,
    sort_desc: bool = True
) -> List[Review]:
    """
    Retrieve all reviews associated with a hotel.
    
    Optional filters:
    - min_rating: filters reviews with rating >= min_rating
    - only_with_text: filters reviews that include a non-empty comment
    - sort_desc: sort reviews by newest first (default True)
    """
    query = db.query(Review).join(Review.booking).join(Booking.room).filter(
        Room.hotel_id == hotel_id
    )

    if min_rating:
        query = query.filter(Review.rating >= min_rating)
    
    if only_with_text:
        query = query.filter(Review.text.isnot(None)).filter(Review.text != "")

    if sort_desc:
        query = query.order_by(Review.id.desc())  # or use created_at if you have
    else:
        query = query.order_by(Review.id.asc())

    return query.all()


def delete_review(db: Session, review_id: int) -> bool:
    """
    Delete a review by its ID.
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return False

    db.delete(review)
    try:
        db.commit()
        return True
    except:
        db.rollback()
        return False
