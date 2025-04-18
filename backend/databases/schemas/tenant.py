from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

# Base schema (shared attributes)
class TenantBase(BaseModel):
    tenant_name: str
    configuration: Optional[Dict[str, Any]] = None

# Schema for creation
class TenantCreate(TenantBase):
    pass

# Schema for update
class TenantUpdate(BaseModel):
    tenant_name: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None

# Schema for read (e.g., responses)
class TenantRead(TenantBase):
    tenant_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
