from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List

from config.database import get_db
from schemas.hotel_photo import HotelPhotoCreate, HotelPhotoRead
from crud.hotel_photo import create_hotel_photo, get_photos_by_hotel, delete_hotel_photo
from services.photo_service import save_image_to_disk, delete_image_file, generate_image_url

router = APIRouter(prefix="/photos", tags=["Hotel Photos"])


@router.post("/", response_model=HotelPhotoRead, status_code=status.HTTP_201_CREATED)
def upload_photo(
    hotel_id: int,
    file: UploadFile,
    caption: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if not file:
        raise HTTPException(status_code=400, detail="File is required")

    try:
        file_path = save_image_to_disk(file)
        image_url = generate_image_url(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

    photo_data = HotelPhotoCreate(
        image_url=image_url,
        hotel_id=hotel_id,
        caption=caption,
        is_cover=None
    )
    photo = create_hotel_photo(db, photo_data)
    if not photo:
        raise HTTPException(status_code=400, detail="Failed to save photo to database")

    return photo


@router.get("/hotel/{hotel_id}", response_model=List[HotelPhotoRead])
def list_photos(hotel_id: int, db: Session = Depends(get_db)):
    return get_photos_by_hotel(db, hotel_id)


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    from crud.hotel_photo import get_photo_by_id  # ensure exists

    photo = get_photo_by_id(db, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    delete_image_file(photo.image_url)
    success = delete_hotel_photo(db, photo_id)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete photo")
