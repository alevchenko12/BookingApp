# RoomAvailability Model (room_availability.py)
from sqlalchemy import Column, Integer, Date, Boolean, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class RoomAvailability(Base):
    __tablename__ = "room_availability"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False, index=True)
    is_available = Column(Boolean, default=False)  # False means booked or blocked, True means available
    price_override = Column(Float, nullable=True)  # Optional custom price for the room on this date
    
    room = relationship("Room", back_populates="availability")
