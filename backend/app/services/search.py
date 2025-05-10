from math import ceil
from typing import List
from sqlalchemy.orm import Session
from app.models.hotel import Hotel
from app.schemas.search import HotelSearchRequest, HotelSearchResult
from app.crud.hotel import search_hotels
from app.crud.room import get_rooms_by_hotel_and_guests
from app.crud import country as crud_country
from app.crud import city as crud_city
from app.crud.room_availability import is_room_available_for_range


def perform_hotel_search(db: Session, search_in: HotelSearchRequest) -> List[HotelSearchResult]:
    city_name = None
    country_name = search_in.destination.strip()

    # Handle "City, Country" format
    if "," in country_name:
        parts = [p.strip() for p in country_name.split(",")]
        if len(parts) >= 2:
            city_name = parts[0]
            country_name = parts[1]

    # Look up country
    country = crud_country.get_country_by_name(db, country_name)
    if not country:
        return []

    country_id = country.id

    # Look up city
    city_id = None
    if city_name:
        city = crud_city.get_city_by_name_and_country(db, city_name, country_id)
        if city:
            city_id = city.id

    # Calculate guests per room
    guests_per_room = ceil(search_in.adults / search_in.rooms)

    # Search hotels
    hotels = search_hotels(db, country_id=country_id, city_id=city_id)
    results: List[HotelSearchResult] = []

    for hotel in hotels:
        rooms = get_rooms_by_hotel_and_guests(db, hotel.id, guests_per_room)
        available_rooms = [
            room for room in rooms if is_room_available_for_range(
                db, room.id, search_in.check_in, search_in.check_out
            )
        ]

        if len(available_rooms) >= search_in.rooms:
            # Safe retrieval of city and country name
            city_name_safe = getattr(hotel.city, "name", None)
            country_name_safe = None

            country_id_from_city = getattr(hotel.city, "country_id", None)
            if country_id_from_city:
                country_obj = crud_country.get_country_by_id(db, country_id_from_city)
                if country_obj:
                    country_name_safe = getattr(country_obj, "name", None)

            # Retrieve cover image URL
            cover_image_url = None
            if hotel.photos:
                cover_photo = next(
                    (p for p in hotel.photos if str(p.is_cover).lower() == "true"), None
                )
                cover_image_url = cover_photo.image_url if cover_photo else hotel.photos[0].image_url

            results.append(HotelSearchResult(
                id=hotel.id,
                name=hotel.name,
                address=hotel.address,
                city=city_name_safe,
                country=country_name_safe,
                stars=hotel.stars,
                lowest_price=min((r.price_per_night for r in available_rooms), default=None),
                cover_image_url=cover_image_url,
                available_room_ids=[r.id for r in available_rooms]
            ))

    return results
