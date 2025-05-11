from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.config.database import get_db
from app.models.user import User
from app.schemas.hotel import HotelCreate, HotelRead, HotelUpdate, HotelWithRelations
from app.crud.hotel import (
    create_hotel, get_hotel_by_id, get_all_hotels,
    delete_hotel, update_hotel, search_hotels, get_hotels_by_owner
)
from app.crud.review import get_reviews_for_hotel
from app.schemas.search import HotelSearchRequest, HotelSearchResult
from app.services.search import perform_hotel_search

from app.models.hotel import Hotel
from app.models.city import City
from app.models.country import Country
from app.models.review import Review
from app.models.user import User
from app.schemas.search_detail import HotelDetailResponse

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

@router.get("/owner/{owner_id}")
def hotels_by_owner(owner_id: int, db: Session = Depends(get_db)):
    """
    Get all hotels created by a specific user (owner), including owner info.
    """
    hotels = get_hotels_by_owner(db, owner_id)

    if not hotels:
        raise HTTPException(status_code=404, detail="No hotels found for this owner")

    return [
        {
            "id": hotel.id,
            "name": hotel.name,
            "address": hotel.address,
            "description": hotel.description,
            "stars": hotel.stars,
            "latitude": hotel.latitude,
            "longitude": hotel.longitude,
            "city": {
                "id": hotel.city.id,
                "name": hotel.city.name
            } if hotel.city else None,
            "owner": {
                "id": hotel.owner.id,
                "first_name": hotel.owner.first_name,
                "last_name": hotel.owner.last_name,
                "email": hotel.owner.email
            } if hotel.owner else None,
            "rooms": hotel.rooms,
            "photos": hotel.photos
        }
        for hotel in hotels
    ]


@router.get("/my-hotels", response_model=List[HotelRead])
def get_my_hotels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get hotels owned by the currently authenticated user.
    """
    return get_hotels_by_owner(db, current_user.id)

# NEW: Advanced Hotel Search with Availability & Destination logic
@router.post("/search-available", response_model=List[HotelSearchResult])
def search_available_hotels(
    request: HotelSearchRequest,
    db: Session = Depends(get_db)
):
    return perform_hotel_search(db, request)




@router.get("/{hotel_id}/details", response_model=HotelDetailResponse)
def get_hotel_detail(hotel_id: int, db: Session = Depends(get_db)):
    hotel = (
        db.query(Hotel)
        .options(
            joinedload(Hotel.city).joinedload(City.country),
            joinedload(Hotel.photos),
            joinedload(Hotel.rooms)
        )
        .filter(Hotel.id == hotel_id)
        .first()
    )

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    # Get reviews separately via Booking → Room → Hotel
    reviews = get_reviews_for_hotel(db, hotel_id=hotel_id)

    return {
        "id": hotel.id,
        "name": hotel.name,
        "address": hotel.address,
        "description": hotel.description,
        "stars": hotel.stars,
        "latitude": hotel.latitude,
        "longitude": hotel.longitude,
        "city": hotel.city.name,
        "country": hotel.city.country.name if hotel.city and hotel.city.country else None,
        "photos": [p.image_url for p in hotel.photos],
        "rooms": hotel.rooms,
        "reviews": [
            {
                "id": r.id,
                "rating": r.rating,
                "text": r.text,
                "user_name": r.user.first_name if r.user else "Anonymous"
            }
            for r in reviews
        ],
    }