from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # BookingID
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # Reference to User, allows NULL
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)  # Reference to Room, allows NULL
    booking_date = Column(Date, nullable=False)  # Date when the booking was made
    check_in_date = Column(Date, nullable=False)  # Check-in date
    check_out_date = Column(Date, nullable=False)  # Check-out date
    status = Column(String(50), nullable=False, default="pending")  # Booking status
    additional_info = Column(String(500), nullable=True)  # Additional information (e.g., number of guests, guest names)
    
    # Relationship to User (Many-to-One)
    user = relationship("User", back_populates="bookings")  # Linking to User table
    # Relationship to Room (Many-to-One)
    room = relationship("Room", back_populates="bookings")  # Linking to Room table

    # One-to-One Relationship with Payment
    payment = relationship("Payment", back_populates="booking", uselist=False, cascade="all, delete-orphan")  # Automatically delete payment when booking is deleted

    # One-to-Many Relationship with Reviews
    reviews = relationship("Review", back_populates="booking", cascade="none")  # No cascade delete for reviews

    # Custom methods to handle booking cancellation when the room is deleted
    def cancel_booking(self):
        self.status = "cancelled"
        self.room = None  # Optionally set room to None (or keep a reference to the canceled room)
