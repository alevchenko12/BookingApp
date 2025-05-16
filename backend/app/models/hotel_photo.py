from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.config.database import Base

class HotelPhoto(Base):
    __tablename__ = "hotel_photos"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    image_url = Column(String(500), nullable=False)  # URL to the photo
    caption = Column(String(255), nullable=True)     # Optional caption for the image
    is_cover = Column(Boolean, nullable=True, default=False)     # Optional: mark cover image

    # Relationship
    hotel = relationship("Hotel", back_populates="photos")
