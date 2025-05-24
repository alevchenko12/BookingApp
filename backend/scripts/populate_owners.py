from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.user_role import UserRole

# List of owner user IDs
owner_user_ids = [14, 15, 16]

# Role to assign
ROLE_NAME = "owner"

db: Session = SessionLocal()
inserted = 0
skipped = 0

for user_id in owner_user_ids:
    existing = db.query(UserRole).filter_by(user_id=user_id, role_name=ROLE_NAME).first()
    if existing:
        print(f"⚠️ Role '{ROLE_NAME}' already exists for user {user_id}, skipping.")
        skipped += 1
        continue

    role = UserRole(user_id=user_id, role_name=ROLE_NAME)
    db.add(role)
    db.commit()
    print(f"✅ Assigned role '{ROLE_NAME}' to user {user_id}")
    inserted += 1

db.close()
print(f"\nInserted: {inserted}, Skipped: {skipped}")
