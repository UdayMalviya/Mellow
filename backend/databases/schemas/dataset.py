# schemas/dataset.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DatasetBase(BaseModel):
    tenant_id: int
    dataset_name: str
    description: Optional[str] = None
    source_id: int

class DatasetCreate(DatasetBase):
    pass

class DatasetUpdate(BaseModel):
    dataset_name: Optional[str] = None
    description: Optional[str] = None
    source_id: Optional[int] = None

class DatasetOut(DatasetBase):
    dataset_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
