# schemas/cache.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

class CacheBase(BaseModel):
    cache_key: str
    cache_value: Optional[Any] = None
    expires_at: datetime

class CacheCreate(CacheBase):
    pass

class CacheUpdate(BaseModel):
    cache_value: Optional[Any]
    expires_at: Optional[datetime]

class CacheOut(CacheBase):
    cache_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
