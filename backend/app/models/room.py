from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    room_type = Column(String(100), nullable=False)  # e.g., "Single", "Double", "Suite"
    price_per_night = Column(Float, nullable=False)  # Price per night for the room
    capacity = Column(Integer, nullable=False)  # Max number of people the room can accommodate
    description = Column(String(500), nullable=True)  # Room description
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="SET NULL"), nullable=True)  # Keep room even if hotel is deleted

    # Room facilities (attributes)
    has_wifi = Column(Boolean, default=False)  # Whether the room has Wi-Fi
    allows_pets = Column(Boolean, default=False)  # Whether the room allows pets
    has_air_conditioning = Column(Boolean, default=False)  # Whether the room has A/C
    has_tv = Column(Boolean, default=False)  # Whether the room has a TV
    has_minibar = Column(Boolean, default=False)  # Whether the room has a minibar
    has_balcony = Column(Boolean, default=False)  # Whether the room has a balcony
    has_kitchen = Column(Boolean, default=False)  # Whether the room has a kitchen
    has_safe = Column(Boolean, default=False)  # Whether the room has a safe

    # Cancellation policy (can be implemented using Enum)
    cancellation_policy = Column(String(255), nullable=True)  # e.g., "Flexible", "Non-refundable"

    # Relationships with hotel
    hotel = relationship("Hotel", back_populates="rooms")

    # One-to-Many: Room can have multiple bookings (No cascade delete on the Room side)
    bookings = relationship("Booking", back_populates="room", cascade="none")   

    # One-to-Many: Room can have multiple availability records
    availability = relationship("RoomAvailability", back_populates="room", cascade="all, delete-orphan")