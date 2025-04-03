# app/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class User(Base):
    __tablename__ = 'users'

    # Auto-generated unique ID (Primary Key)
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # Full name (first and last names are mandatory)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)

    # Email (Unique, Not Null)
    email = Column(String, unique=True, nullable=False, index=True)

    # Phone number (Optional, nullable)
    phone = Column(String, nullable=True)

    # Password hash (For security, passwords are never stored in plain text)
    password_hash = Column(String, nullable=False)

    # Optional relationship with other tables (e.g., Bookings, etc.)
    # bookings = relationship("Booking", back_populates="user")
