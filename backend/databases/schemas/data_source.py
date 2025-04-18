# schemas/data_source.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DataSourceBase(BaseModel):
    tenant_id: int
    source_name: str
    source_type: str
    configuration: Optional[dict] = None

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceUpdate(BaseModel):
    source_name: Optional[str] = None
    source_type: Optional[str] = None
    configuration: Optional[dict] = None

class DataSourceOut(DataSourceBase):
    source_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
