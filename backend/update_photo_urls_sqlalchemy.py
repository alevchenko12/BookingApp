from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.hotel_photo import HotelPhoto  # Make sure import path is correct

# URL replacement config
OLD_BASE_URL = "http://10.0.2.2:8000/static/uploads/"
NEW_BASE_URL = "http://192.168.1.104:8000/static/uploads/"
PHOTO_ID_RANGE = range(8, 17)  # 8 to 16 inclusive

def update_photo_urls():
    updated = 0
    skipped = 0

    with SessionLocal() as db:
        photos = db.query(HotelPhoto).filter(HotelPhoto.id.in_(PHOTO_ID_RANGE)).all()

        for photo in photos:
            if photo.image_url.startswith(OLD_BASE_URL):
                filename = photo.image_url.split("/")[-1]
                new_url = NEW_BASE_URL + filename

                print(f"🔄 Updating ID {photo.id}")
                print(f"  Old URL: {photo.image_url}")
                print(f"  New URL: {new_url}")

                photo.image_url = new_url
                updated += 1
            else:
                print(f"⏭️ Skipping ID {photo.id} (URL not matching old base)")
                skipped += 1

        db.commit()
        print(f"\n✅ Done. Updated: {updated}, Skipped: {skipped}")

# Run it
if __name__ == "__main__":
    update_photo_urls()
