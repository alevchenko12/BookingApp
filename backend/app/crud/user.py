from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from app.models.user import User
from app.models.booking import Booking
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Retrieve a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Retrieve a user by their email address."""
    return db.query(User).filter(User.email == email.strip().lower()).first()


def create_user(db: Session, user_in: UserCreate) -> Optional[User]:
    """Create a new user with a unique email and hashed password."""
    existing = get_user_by_email(db, user_in.email)
    if existing:
        return None

    user = User(
        first_name=user_in.first_name.strip(),
        last_name=user_in.last_name.strip(),
        email=user_in.email.lower().strip(),
        phone=user_in.phone.strip() if user_in.phone else None,
        password_hash=pwd_context.hash(user_in.password)
    )

    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        return None


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user only if they have no pending or confirmed bookings."""
    user = get_user_by_id(db, user_id)
    if not user:
        return False

    active_statuses = {"pending", "confirmed"}
    if any(b.status in active_statuses for b in user.bookings):
        return False

    db.delete(user)
    try:
        db.commit()
        return True
    except:
        db.rollback()
        return False


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update an existing user's profile fields."""
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, field, value.strip() if isinstance(value, str) else value)

    db.commit()
    db.refresh(user)
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check whether a raw password matches a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user credentials by email and password."""
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.password_hash):
        return user
    return None
