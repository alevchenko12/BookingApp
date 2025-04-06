from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # Review ID
    rating = Column(Integer, nullable=False)  # Rating (e.g., 1-5)
    text = Column(String(500), nullable=True)  # Review Text
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # Reference to User (nullable)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True)  # Reference to Booking (nullable)

    # Relationships
    user = relationship("User", back_populates="reviews", uselist=False)  # One-to-One relationship with User
    booking = relationship("Booking", back_populates="reviews", uselist=False)  # One-to-One relationship with Booking

    def __repr__(self):
        return f"<Review(id={self.id}, user_id={self.user_id}, rating={self.rating}, text={self.text})>"
