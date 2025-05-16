# backend/app/main.py

from fastapi import FastAPI
from app.config.settings import settings
from fastapi.staticfiles import StaticFiles

import os

# Routers
from app.routers import city, country, user, user_role, hotel, room, room_availability, hotel_photo, booking, cancellation, payment, review, location
app = FastAPI(
    title="Booking API",
    version="1.0.0"
)

UPLOAD_DIR = os.path.join("static", "uploads")

app.mount("/static/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Register all routers
app.include_router(user.router)
app.include_router(hotel.router)
app.include_router(city.router)
app.include_router(country.router)
app.include_router(hotel_photo.router)
app.include_router(user_role.router)
app.include_router(room.router)
app.include_router(room_availability.router)
app.include_router(booking.router)
app.include_router(cancellation.router)
app.include_router(payment.router)
app.include_router(review.router)
app.include_router(location.router)