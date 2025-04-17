from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List


# Role schemas (for nested relationship with User)
class RoleRead(BaseModel):
    role_id: int
    role_name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Base user schema
class UserBase(BaseModel):
    username: str
    email: EmailStr


# Schema for creating a new user
class UserCreate(UserBase):
    password: str


# Schema for updating user
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# Basic read schema (e.g., for lists or brief views)
class UserRead(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Full detail output including timestamps
class UserOut(UserRead):
    created_at: datetime
    updated_at: datetime


# Output with associated roles (nested)
class UserWithRoles(UserOut):
    roles: List[RoleRead] = []


# Optional minimal response
class UserMinimal(BaseModel):
    user_id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
