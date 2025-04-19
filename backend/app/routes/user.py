from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from schemas.user import UserCreate, UserRead, UserUpdate, UserWithRelations
from crud import user as crud_user
from app.config.database import get_db  

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user. Requires unique email.
    """
    user = crud_user.create_user(db, user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    return user


@router.get("/{user_id}", response_model=UserWithRelations)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a single user by ID with full profile.
    """
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update fields for a specific user.
    """
    user = crud_user.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or update failed")
    return user


@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user only if no active bookings.
    """
    success = crud_user.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete user: active bookings or not found"
        )
    return {"message": "User deleted successfully"}


@router.post("/login", response_model=UserRead)
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    """
    Authenticate user by email and password.
    """
    user = crud_user.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return user
