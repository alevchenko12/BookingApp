from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.config.database import get_db
from app.models.user import User
from app.schemas.hotel import HotelCreate, HotelRead, HotelUpdate, HotelWithRelations
from app.crud.hotel import (
    create_hotel, get_hotel_by_id, get_all_hotels,
    delete_hotel, update_hotel, search_hotels
)

router = APIRouter(prefix="/hotels", tags=["Hotels"])


# 🧪 MOCK AUTH (replace with real auth)
def get_current_user() -> User:
    return User(id=1, first_name="Test", last_name="User", email="test@example.com", password_hash="...")


@router.post("/", response_model=HotelRead, status_code=status.HTTP_201_CREATED)
def create_new_hotel(
    hotel_in: HotelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Override owner_id with current authenticated user
    hotel_data = hotel_in.model_copy(update={"owner_id": current_user.id})
    
    hotel = create_hotel(db, hotel_data)
    if not hotel:
        raise HTTPException(status_code=400, detail="Hotel could not be created.")
    return hotel


@router.get("/", response_model=List[HotelRead])
def list_all_hotels(db: Session = Depends(get_db)):
    return get_all_hotels(db)


@router.get("/{hotel_id}", response_model=HotelWithRelations)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = get_hotel_by_id(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel


@router.put("/{hotel_id}", response_model=HotelRead)
def update_existing_hotel(
    hotel_id: int,
    hotel_update: HotelUpdate,
    db: Session = Depends(get_db)
):
    updated = update_hotel(db, hotel_id, hotel_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Hotel not found or update failed")
    return updated


@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_hotel(hotel_id: int, db: Session = Depends(get_db)):
    success = delete_hotel(db, hotel_id)
    if not success:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return


@router.get("/search/", response_model=List[HotelRead])
def search_hotel_list(
    db: Session = Depends(get_db),
    country_id: Optional[int] = None,
    city_id: Optional[int] = None,
    min_stars: Optional[int] = None,
    center_lat: Optional[float] = None,
    center_lon: Optional[float] = None,
    radius_km: Optional[float] = None,
):
    return search_hotels(
        db=db,
        country_id=country_id,
        city_id=city_id,
        min_stars=min_stars,
        center_lat=center_lat,
        center_lon=center_lon,
        radius_km=radius_km,
    )

@router.get("/owner/{owner_id}", response_model=List[HotelRead])
def get_hotels_by_owner(owner_id: int, db: Session = Depends(get_db)):
    """
    Get all hotels created by a specific user (owner).
    """
    hotels = get_hotels_by_owner(db, owner_id)
    return hotels


@router.get("/my-hotels", response_model=List[HotelRead])
def get_my_hotels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get hotels owned by the currently authenticated user.
    """
    return get_hotels_by_owner(db, current_user.id)
