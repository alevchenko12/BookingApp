from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from models.hotel_photo import HotelPhoto
from models.hotel import Hotel
from schemas.hotel_photo import HotelPhotoCreate


def create_hotel_photo(db: Session, photo_in: HotelPhotoCreate) -> Optional[HotelPhoto]:
    """Upload and store a new photo for a hotel after verifying hotel exists."""
    hotel = db.query(Hotel).filter(Hotel.id == photo_in.hotel_id).first()
    if not hotel:
        return None  # Invalid FK — hotel does not exist

    photo = HotelPhoto(
        image_url=str(photo_in.image_url),
        caption=photo_in.caption.strip() if photo_in.caption else None,
        is_cover=photo_in.is_cover.strip() if photo_in.is_cover else None,
        hotel_id=photo_in.hotel_id
    )

    db.add(photo)
    try:
        db.commit()
        db.refresh(photo)
        return photo
    except IntegrityError:
        db.rollback()
        return None


def get_photos_by_hotel(db: Session, hotel_id: int) -> List[HotelPhoto]:
    """Retrieve all photos for a given hotel."""
    return db.query(HotelPhoto).filter(HotelPhoto.hotel_id == hotel_id).all()


def delete_hotel_photo(db: Session, photo_id: int) -> bool:
    """Delete a photo by its ID."""
    photo = db.query(HotelPhoto).filter(HotelPhoto.id == photo_id).first()
    if not photo:
        return False

    db.delete(photo)
    try:
        db.commit()
        return True
    except:
        db.rollback()
        return False


def set_cover_photo(db: Session, hotel_id: int, photo_id: int) -> bool:
    """Set a specific photo as the cover for a hotel (unset all others)."""
    photos = db.query(HotelPhoto).filter(HotelPhoto.hotel_id == hotel_id).all()
    if not any(p.id == photo_id for p in photos):
        return False  # Provided photo doesn't belong to the hotel

    # Unset previous cover
    for photo in photos:
        photo.is_cover = "yes" if photo.id == photo_id else None

    try:
        db.commit()
        return True
    except:
        db.rollback()
        return False
