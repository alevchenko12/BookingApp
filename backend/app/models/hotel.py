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

    # Relationships
    city = relationship("City", back_populates="hotels", cascade="all, delete-orphan")  # Delete hotels when a city is deleted
    rooms = relationship("Room", back_populates="hotel", cascade="none")  # No delete cascade on rooms
    photos = relationship("HotelPhoto", back_populates="hotel", cascade="all, delete")