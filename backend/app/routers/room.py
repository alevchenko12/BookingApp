from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.config.database import get_db
from app.crud import room as crud_room
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomRead, RoomUpdate
from app.models.hotel import Hotel

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
def create_room(
    room_in: RoomCreate,
    db: Session = Depends(get_db),
):
    room = crud_room.create_room(db, room_in)
    if not room:
        raise HTTPException(status_code=400, detail="Room could not be created. Check hotel ID.")
    return room


@router.get("/{room_id}")
def get_room_with_hotel(room_id: int, db: Session = Depends(get_db)):
    room = crud_room.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    hotel = room.hotel
    return {
        "id": room.id,
        "name": room.name,
        "room_type": room.room_type,
        "price_per_night": room.price_per_night,
        "capacity": room.capacity,
        "description": room.description,
        "cancellation_policy": room.cancellation_policy,
        "has_wifi": room.has_wifi,
        "allows_pets": room.allows_pets,
        "has_air_conditioning": room.has_air_conditioning,
        "has_tv": room.has_tv,
        "has_minibar": room.has_minibar,
        "has_balcony": room.has_balcony,
        "has_kitchen": room.has_kitchen,
        "has_safe": room.has_safe,
        "hotel": {
            "id": hotel.id,
            "name": hotel.name,
            "address": hotel.address,
        } if hotel else None
    }


@router.put("/{room_id}", response_model=RoomRead)
def update_room(
    room_id: int,
    room_update: RoomUpdate,
    db: Session = Depends(get_db),
):
    updated = crud_room.update_room(db, room_id, room_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Room not found or update failed")
    return updated


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    success = crud_room.delete_room(db, room_id)
    if not success:
        raise HTTPException(status_code=404, detail="Room not found")
    return


@router.get("/hotel/{hotel_id}", response_model=List[RoomRead])
def get_rooms_by_hotel(hotel_id: int, db: Session = Depends(get_db)):
    return crud_room.get_rooms_by_hotel_id(db, hotel_id)


@router.get("/search/", response_model=List[RoomRead])
def filter_rooms(
    db: Session = Depends(get_db),
    hotel_id: Optional[int] = None,
    room_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    has_wifi: Optional[bool] = None,
    allows_pets: Optional[bool] = None,
    has_air_conditioning: Optional[bool] = None,
    has_tv: Optional[bool] = None,
    has_minibar: Optional[bool] = None,
    has_balcony: Optional[bool] = None,
    has_kitchen: Optional[bool] = None,
    has_safe: Optional[bool] = None,
    min_capacity: Optional[int] = None,
):
    return crud_room.filter_rooms(
        db=db,
        hotel_id=hotel_id,
        room_type=room_type,
        min_price=min_price,
        max_price=max_price,
        has_wifi=has_wifi,
        allows_pets=allows_pets,
        has_air_conditioning=has_air_conditioning,
        has_tv=has_tv,
        has_minibar=has_minibar,
        has_balcony=has_balcony,
        has_kitchen=has_kitchen,
        has_safe=has_safe,
        min_capacity=min_capacity,
    )
