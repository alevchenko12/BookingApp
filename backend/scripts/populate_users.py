from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.schemas.user import UserCreate
from app.crud.user import create_user
from app.models.user import User
from app.models.user_role import UserRole
from app.models.review import Review
from app.models.hotel import Hotel
from sqlalchemy.exc import IntegrityError

# List of users to insert
users = [
    {
        "first_name": "Anastasiia", "last_name": "Levchenko", "email": "nastiya.levchenko@gmail.com",
        "phone": "+38984553290", "password": "BestPassword123"
    },
    {
        "first_name": "Olha", "last_name": "Levchenko", "email": "nastiya.levchenko@knu.ua",
        "phone": "+38975886886", "password": "WorstPassword123"
    },
    {
        "first_name": "Taras", "last_name": "Schevchenko", "email": "taras.schevchenko@email.com",
        "phone": "+12345670003", "password": "charliepass"
    },
    {
        "first_name": "Anna", "last_name": "Avecherkova", "email": "ananas@emeail.com",
        "phone": "+12345670004", "password": "dianapass"
    }
]

db: Session = SessionLocal()

# Step 1: Delete users (and related records if cascade is enabled)
try:
    db.query(UserRole).delete()
    db.query(Review).delete()
    db.query(Hotel).delete()
    db.query(User).delete()
    db.commit()
    print("🗑️ All existing users and related data deleted.")
except Exception as e:
    db.rollback()
    print(f"❌ Error during deletion: {e}")
    db.close()
    exit()

# Step 2: Insert new users
inserted = 0
for u in users:
    user_data = UserCreate(**u)
    created = create_user(db, user_data)
    if created:
        print(f"✅ Created: {created.email}")
        inserted += 1
    else:
        print(f"⚠️ Failed to create: {u['email']}")

db.close()
print(f"\n✅ {inserted} users inserted.")
