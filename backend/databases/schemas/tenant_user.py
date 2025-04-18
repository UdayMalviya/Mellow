# schemas/tenant_user.py
from pydantic import BaseModel, ConfigDict

class TenantUserBase(BaseModel):
    tenant_id: int
    user_id: int

class TenantUserCreate(TenantUserBase):
    pass

class TenantUserOut(TenantUserBase):
    model_config = ConfigDict(from_attributes=True)
