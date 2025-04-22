from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.config.database import get_db
from app.schemas.review import ReviewCreate, ReviewRead, ReviewWithRelations
from app.crud.review import (
    create_review, get_review_by_id, get_reviews_by_user,
    get_reviews_by_booking, get_reviews_for_hotel, delete_review
)
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def submit_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a review for a completed booking. Authenticated users only.
    """
    review_data = review_in.model_copy(update={"user_id": current_user.id})
    review = create_review(db, review_data)
    if not review:
        raise HTTPException(
            status_code=400,
            detail="Review creation failed. Make sure booking is yours and completed, or review already exists."
        )
    return review


@router.get("/user/me", response_model=List[ReviewRead])
def get_my_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all reviews submitted by the current user.
    """
    return get_reviews_by_user(db, current_user.id)


@router.get("/booking/{booking_id}", response_model=List[ReviewWithRelations])
def get_reviews_for_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Get all reviews for a specific booking (usually 1).
    """
    return get_reviews_by_booking(db, booking_id)

@router.get("/hotel/{hotel_id}", response_model=List[ReviewWithRelations])
def get_reviews_for_hotel_endpoint(
    hotel_id: int,
    min_rating: Optional[int] = None,  # None means "no filter"
    only_with_text: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get all reviews for a specific hotel with optional filters.
    """
    return get_reviews_for_hotel(
        db=db,
        hotel_id=hotel_id,
        min_rating=min_rating,
        only_with_text=only_with_text
    )


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review_by_id(review_id: int, db: Session = Depends(get_db)):
    """
    Admin use: Delete a review by ID.
    """
    success = delete_review(db, review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")
