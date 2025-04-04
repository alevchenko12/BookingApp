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
    available = Column(Boolean, default=True)  # Whether the room is available for booking
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)  # The hotel the room belongs to

    # Room facilities (attributes)
    has_wifi = Column(Boolean, default=False)  # Whether the room has Wi-Fi
    allows_pets = Column(Boolean, default=False)  # Whether the room allows pets
    has_air_conditioning = Column(Boolean, default=False)  # Whether the room has A/C
    has_tv = Column(Boolean, default=False)  # Whether the room has a TV
    has_minibar = Column(Boolean, default=False)  # Whether the room has a minibar
    has_balcony = Column(Boolean, default=False)  # Whether the room has a balcony
    has_kitchen = Column(Boolean, default=False)  # Whether the room has a kitchen
    has_safe = Column(Boolean, default=False)  # Whether the room has a safe

    # Cancellation policy (can be implemented using Enum or String)
    cancellation_policy = Column(String(255), nullable=True)  # e.g., "Flexible", "Non-refundable"

    # Ratings and Reviews will be handled separately (see below)
    reviews = relationship("Review", back_populates="room")
    
    # Relationships with hotel
    hotel = relationship("Hotel", back_populates="rooms")
