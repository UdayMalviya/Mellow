from pydantic import BaseModel, ConfigDict
from typing import Optional


class PermissionBase(BaseModel):
    permission_name: str
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    permission_name: Optional[str] = None
    description: Optional[str] = None


class PermissionRead(PermissionBase):
    permission_id: int

    model_config = ConfigDict(from_attributes=True)
