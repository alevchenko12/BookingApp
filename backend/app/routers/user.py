from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.config.database import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserWithRelations
from app.schemas.token import TokenWithUser
from app.crud import user as crud_user
from app.services.auth import create_access_token
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.token import LoginRequest  
from app.services.email_service import send_registration_email
from app.services.email_service import send_verification_email
from jose import jwt, JWTError
from app.config.settings import settings

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# -----------------------
# PUBLIC: Register & Login
# -----------------------

@router.post("/register", response_model=TokenWithUser, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user. Returns access token and user info.
    """
    user = crud_user.create_user(db, user_in)
    if not user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Send welcome email
    try:
        send_registration_email(user.email, user.first_name)
    except Exception as e:
        print(f"[Email Error] Failed to send welcome email: {e}")

    token = create_access_token(data={"sub": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

## ADDED usage of json body
@router.post("/login", response_model=TokenWithUser)
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/register-initiate", status_code=200)
def register_initiate(user_in: UserCreate):
    token = jwt.encode(user_in.model_dump(), settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    send_verification_email(user_in.email, token)
    return {"message": "Verification email sent. Please check your inbox."}


@router.get("/verify-registration")
def verify_registration(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_data = UserCreate(**payload)

        existing = crud_user.get_user_by_email(db, user_data.email)
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")

        user = crud_user.create_user(db, user_data)
        if not user:
            raise HTTPException(status_code=500, detail="User creation failed")

        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "user": user}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

# -----------------------
# PROTECTED: User Self-Service
# -----------------------

@router.get("/me", response_model=UserWithRelations)
def get_my_profile(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Get the currently authenticated user's full profile.
    """
    return current_user


@router.put("/me", response_model=UserRead)
def update_my_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    user_update: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    Update the current user's own profile.
    """
    updated_user = crud_user.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/me", response_model=dict)
def delete_my_profile(
     current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db), 
):
    """
    Delete the current user's own profile if no active bookings exist.
    """
    success = crud_user.delete_user(db, current_user.id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot delete user: active bookings or not found")
    return {"message": "User deleted successfully"}

# -----------------------
# ADMIN (optional for future use)
# -----------------------

@router.get("/{user_id}", response_model=UserWithRelations)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Admin use: Get a user by ID.
    """
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/email/{email}", response_model=UserRead)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Admin use: Get a user by email.
    """
    user = crud_user.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
