from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta
from typing import Optional, List

from app.models.booking import Booking
from app.models.room import Room
from app.models.user import User
from app.models.room_availability import RoomAvailability
from app.schemas.booking import BookingCreate, BookingStatusEnum
from app.schemas.room_availability import RoomAvailabilityCreate
from app.schemas.cancellation import CancellationCreate
from app.crud.room_availability import create_availability_entry
from app.crud.room_availability import is_room_available_for_range
from app.crud.cancellation import create_cancellation
from app.schemas.booking import BookingStatusEnum

def create_booking(db: Session, booking_in: BookingCreate) -> Optional[Booking]:
    """
    Create a new booking if the room is available for the selected dates.
    Adds RoomAvailability entries to block the room. Handles race conditions via row locking.
    """

    # 0. Check that date range is valid
    if booking_in.check_in_date >= booking_in.check_out_date:
        return None

    # 1. Validate user and room exist
    if not db.query(User).filter(User.id == booking_in.user_id).first():
        return None
    room = db.query(Room).filter(Room.id == booking_in.room_id).first()
    if not room:
        return None

    # 2. Lock potential availability conflicts before checking
    db.query(RoomAvailability).filter(
        RoomAvailability.room_id == booking_in.room_id,
        RoomAvailability.date >= booking_in.check_in_date,
        RoomAvailability.date < booking_in.check_out_date
    ).with_for_update().all()

    # 3. Check room availability for range (assumes unavailable entries mean blocked)
    if not is_room_available_for_range(db, booking_in.room_id, booking_in.check_in_date, booking_in.check_out_date):
        return None

    # 4. Create booking object
    booking = Booking(
        user_id=booking_in.user_id,
        room_id=booking_in.room_id,
        booking_date=booking_in.booking_date,
        check_in_date=booking_in.check_in_date,
        check_out_date=booking_in.check_out_date,
        status="pending",
        additional_info=booking_in.additional_info.strip() if booking_in.additional_info else None
    )

    db.add(booking)
    try:
        db.commit()
        db.refresh(booking)
    except IntegrityError:
        db.rollback()
        return None

    # 5. Add availability entries (booked days)
    delta = (booking.check_out_date - booking.check_in_date).days
    for i in range(delta):
        day = booking.check_in_date + timedelta(days=i)

        availability_entry = RoomAvailabilityCreate(
            room_id=booking.room_id,
            date=day,
            is_available=False,
            price_override=None
        )

        try:
            create_availability_entry(db, availability_entry)
        except IntegrityError:
            db.rollback()
            return None  # Race condition fallback

    return booking

def get_booking_by_id(db: Session, booking_id: int) -> Optional[Booking]:
    """
    Retrieve a single booking by its ID.
    """
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_bookings_by_user(db: Session, user_id: int) -> List[Booking]:
    """
    Get all bookings associated with a specific user, ordered by check-in.
    """
    return db.query(Booking).filter(Booking.user_id == user_id).order_by(Booking.check_in_date.desc()).all()

def cancel_booking(db: Session, booking_id: int, refund_amount: float = 0.0) -> bool:
    booking = get_booking_by_id(db, booking_id)
    if not booking or booking.status == BookingStatusEnum.cancelled or booking.status == BookingStatusEnum.completed:
        return False

    # Update booking status
    booking.status = BookingStatusEnum.cancelled

    # Create cancellation record (via dedicated CRUD)
    cancellation_data = CancellationCreate(
        booking_id=booking.id,
        cancellation_date=date.today(),
        refund_amount=refund_amount
    )
    cancellation = create_cancellation(db, cancellation_data)
    if not cancellation:
        db.rollback()
        return False

    # Remove availability blocks
    db.query(RoomAvailability).filter(
        RoomAvailability.room_id == booking.room_id,
        RoomAvailability.date >= booking.check_in_date,
        RoomAvailability.date < booking.check_out_date,
        RoomAvailability.is_available == False
    ).delete(synchronize_session=False)

    try:
        db.commit()
        return True
    except:
        db.rollback()
        return False

def mark_booking_as_confirmed(db: Session, booking_id: int) -> bool:
    """
    Update booking status to 'confirmed' after successful payment.
    """
    booking = get_booking_by_id(db, booking_id)
    if not booking or booking.status != BookingStatusEnum.pending:
        return False

    booking.status = BookingStatusEnum.confirmed

    try:
        db.commit()
        db.refresh(booking)
        return True
    except:
        db.rollback()
        return False

#############################
# MUST BE TRIGERRED 
#How to Trigger It?
#Run this once a day (e.g. with Celery, cronjob, or FastAPI’s BackgroundTasks).
#It will silently clean up outdated confirmed bookings and mark them as completed.
#############################
def complete_and_cleanup_bookings(db: Session) -> dict:
    """
    - Mark confirmed bookings as completed if check-out has passed.
    - Cancel pending bookings if check-in has passed and they were never confirmed.
    Returns a summary dictionary.
    """
    today = date.today()
    completed_count = 0
    cancelled_count = 0

    # 1. Complete confirmed bookings where check-out is in the past
    confirmed_bookings = db.query(Booking).filter(
        Booking.status == BookingStatusEnum.confirmed,
        Booking.check_out_date < today
    ).all()

    for booking in confirmed_bookings:
        booking.status = BookingStatusEnum.completed
        completed_count += 1

    # 2. Cancel pending bookings where check-in date is in the past
    expired_pending = db.query(Booking).filter(
        Booking.status == BookingStatusEnum.pending,
        Booking.check_in_date < today
    ).all()

    for booking in expired_pending:
        booking.status = BookingStatusEnum.cancelled
        cancelled_count += 1

    if completed_count > 0 or cancelled_count > 0:
        db.commit()

    return {
        "completed_bookings": completed_count,
        "cancelled_pending_bookings": cancelled_count
    }

from sqlalchemy.orm import Session
from typing import List
from app.models.booking import Booking
from app.models.hotel import Hotel
from app.models.city import City
from app.models.country import Country
from app.models.room import Room
from app.models.payment import Payment
from app.models.hotel_photo import HotelPhoto
from app.schemas.enriched_booking import BookingUiModel


def get_user_bookings_ui(db: Session, user_id: int) -> List[BookingUiModel]:
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
    ui_models = []

    for booking in bookings:
        if not booking.room:
            continue

        room = booking.room
        hotel = room.hotel
        if not hotel:
            continue

        city = hotel.city
        country = city.country if city else None

        cover_photo = (
            db.query(HotelPhoto)
            .filter(HotelPhoto.hotel_id == hotel.id, HotelPhoto.is_cover == True)
            .first()
        )

        payment = db.query(Payment).filter(Payment.booking_id == booking.id).first()
        total_price = f"${payment.amount:.2f}" if payment else None

        ui_models.append(
            BookingUiModel(
                id=booking.id,
                hotel_name=hotel.name,
                address=hotel.address,
                city=city.name if city else "",
                country=country.name if country else "",
                check_in=booking.check_in_date.isoformat(),
                check_out=booking.check_out_date.isoformat(),
                booking_date=booking.booking_date.isoformat(),
                total_price=total_price,
                status=booking.status,
                cover_image_url=cover_photo.image_url if cover_photo else None,
                cancellation_policy=room.cancellation_policy,
                latitude=hotel.latitude,
                longitude=hotel.longitude
            )
        )

    return ui_models
