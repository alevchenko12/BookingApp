from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user_role import UserRoleCreate, UserRoleRead
from app.crud import user_role as crud_user_role
from app.config.database import get_db

router = APIRouter(
    prefix="/roles",
    tags=["User Roles"],
)

@router.post("/assign", response_model=UserRoleRead, status_code=status.HTTP_201_CREATED)
def assign_role(role_in: UserRoleCreate, db: Session = Depends(get_db)):
    """
    Assign a role to a user. Prevents duplicate role assignment.
    """
    role = crud_user_role.assign_user_role(db, role_in)
    if not role:
        raise HTTPException(status_code=404, detail="User not found or role assignment failed")
    return role

@router.get("/user/{user_id}", response_model=List[UserRoleRead])
def get_roles_for_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get all roles for a given user.
    """
    return crud_user_role.get_roles_for_user(db, user_id)

@router.delete("/user/{user_id}/{role_name}", status_code=status.HTTP_204_NO_CONTENT)
def remove_role(user_id: int, role_name: str, db: Session = Depends(get_db)):
    """
    Remove a specific role from a user.
    """
    success = crud_user_role.remove_user_role(db, user_id, role_name)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found for this user")
