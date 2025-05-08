from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.config.database import get_db
from app.schemas.user import ForgotPasswordRequest, VerifyCodeRequest, ResetPasswordRequest
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserWithRelations
from app.schemas.token import TokenWithUser
from app.crud import user as crud_user
from app.services.auth import create_access_token
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.token import LoginRequest  
from app.services.email_service import send_registration_email, send_verification_email, send_reset_code_email
from jose import jwt, JWTError
from app.config.settings import settings
from pydantic import EmailStr
import random


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
    Only used for direct registration without verification (if allowed).
    """
    # Check if user already exists
    existing = crud_user.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Create the user in the DB
    user = crud_user.create_user(db, user_in)
    if not user:
        raise HTTPException(status_code=500, detail="Failed to create user")

    # Send welcome email
    try:
        send_registration_email(user.email, f"{user.first_name} {user.last_name}")
    except Exception as e:
        print(f"[Email Error] Failed to send welcome email: {e}")

    # Return access token and user data
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

reset_codes = {}  # Use Redis/DB in production

# Send reset code
@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    code = str(random.randint(100000, 999999))
    reset_codes[request.email] = code

    try:
        send_reset_code_email(request.email, code)
    except Exception as e:
        print(f"[Email Error] Failed to send reset code: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")

    return {"message": "Reset code sent to your email"}

# Verify code
@router.post("/verify-code")
def verify_code(request: VerifyCodeRequest):
    expected = reset_codes.get(request.email)
    if not expected or request.code != expected:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    return {"message": "Code verified"}

# Reset password
@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    crud_user.update_user_password(db, user, request.new_password)
    reset_codes.pop(request.email, None)
    return {"message": "Password reset successful"}

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

        # Send greeting email here
        try:
            send_registration_email(user.email, f"{user.first_name} {user.last_name}")
        except Exception as e:
            print(f"[Email Error] Failed to send welcome email: {e}")

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
