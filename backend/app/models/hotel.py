from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    stars = Column(Integer, nullable=True)
    description = Column(String(500), nullable=True)

    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Add this relationship
    owner = relationship("User", back_populates="owned_hotels")

    # Relationships
    city = relationship("City", back_populates="hotels")  # Delete hotels when a city is deleted
    rooms = relationship("Room", back_populates="hotel", cascade="none")  # No delete cascade on rooms
    photos = relationship("HotelPhoto", back_populates="hotel", cascade="all, delete")