# schemas/user_role.py
from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserRoleBase(BaseModel):
    user_id: int
    role_id: int

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleRead(UserRoleBase):
    user_id: int
    role_id: int

    model_config = ConfigDict(from_attributes=True) 

class UserRoleUpdate(BaseModel):
    role_id: Optional[int] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
        
