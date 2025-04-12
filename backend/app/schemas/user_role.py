from enum import Enum
from pydantic import BaseModel
from typing import Annotated
from pydantic import StringConstraints

# Enum for strict role control
class RoleEnum(str, Enum):
    guest = "guest"
    manager = "manager"

# Base schema with validated role name
class UserRoleBase(BaseModel):
    role_name: RoleEnum

# Create schema: only role_name + user_id (id is auto-assigned in DB)
class UserRoleCreate(UserRoleBase):
    user_id: int

# Read schema: what you return to frontend
class UserRoleRead(UserRoleBase):
    id: int

    class Config:
        orm_mode = True
