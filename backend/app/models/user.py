from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class User(Base):
    __tablename__ = 'users'

    # Auto-generated unique ID (Primary Key)
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # Full name (first and last names are mandatory)
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)

    # Email (Unique, Not Null)
    email = Column(String(100), unique=True, nullable=False, index=True)

    # Phone number (Optional, nullable)
    phone = Column(String(15), nullable=True)

    # Password hash (For security, passwords are never stored in plain text)
    password_hash = Column(String(200), nullable=False)

    # Relationship with bookings
    bookings = relationship("Booking", back_populates="user", cascade="none")  # No cascade delete

    # Relationship with reviews (One-to-Many)
    reviews = relationship("Review", back_populates="user", cascade="none")  # No cascade delete for reviews

    owned_hotels = relationship("Hotel", back_populates="owner", cascade="all, delete-orphan")

    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
