from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.user_role import UserRole
from sqlalchemy.exc import IntegrityError

# List of user IDs to assign the role
user_ids = [14, 15, 16, 17]

# Role name to assign
ROLE_NAME = "guest"  # 🔁 Change to "tourist" if you prefer

db: Session = SessionLocal()
inserted = 0
skipped = 0

for uid in user_ids:
    # Check if the user already has this role
    existing = db.query(UserRole).filter_by(user_id=uid, role_name=ROLE_NAME).first()
    if existing:
        print(f"⚠️ Role '{ROLE_NAME}' already exists for user {uid}, skipping.")
        skipped += 1
        continue

    role = UserRole(user_id=uid, role_name=ROLE_NAME)
    db.add(role)
    try:
        db.commit()
        print(f"✅ Assigned role '{ROLE_NAME}' to user {uid}")
        inserted += 1
    except IntegrityError:
        db.rollback()
        print(f"❌ Failed to assign role to user {uid} (IntegrityError)")

db.close()
print(f"\nInserted: {inserted}, Skipped: {skipped}")
