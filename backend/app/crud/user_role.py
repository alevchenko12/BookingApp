from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from app.models.user_role import UserRole
from app.schemas.user_role import UserRoleCreate
from app.models.user import User


def assign_user_role(db: Session, role_in: UserRoleCreate) -> Optional[UserRole]:
    """Assign a new role to a user (e.g. guest, manager), after validating user exists and role is not already assigned."""

    # FK check: make sure user exists
    user = db.query(User).filter(User.id == role_in.user_id).first()
    if not user:
        return None

    # Prevent assigning the same role more than once
    existing = db.query(UserRole).filter(
        UserRole.user_id == role_in.user_id,
        UserRole.role_name == role_in.role_name
    ).first()
    if existing:
        return existing  # Role already assigned — return existing or handle in route

    # Assign the role
    role = UserRole(user_id=role_in.user_id, role_name=role_in.role_name)

    db.add(role)
    try:
        db.commit()
        db.refresh(role)
        return role
    except IntegrityError:
        db.rollback()
        return None


def get_roles_for_user(db: Session, user_id: int) -> List[UserRole]:
    """Retrieve all roles assigned to a specific user."""
    return db.query(UserRole).filter(UserRole.user_id == user_id).all()


def remove_user_role(db: Session, user_id: int, role_name: str) -> bool:
    """Remove a specific role from a user."""
    role = db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_name == role_name
    ).first()

    if not role:
        return False

    db.delete(role)
    try:
        db.commit()
        return True
    except:
        db.rollback()
        return False
