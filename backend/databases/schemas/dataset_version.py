# schemas/dataset_version.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DatasetVersionBase(BaseModel):
    dataset_id: int
    version_number: str
    preprocessing_steps: Optional[dict] = None  # JSONB
    storage_location: Optional[str] = None

class DatasetVersionCreate(DatasetVersionBase):
    pass

class DatasetVersionUpdate(BaseModel):
    version_number: Optional[str] = None
    preprocessing_steps: Optional[dict] = None
    storage_location: Optional[str] = None

class DatasetVersionOut(DatasetVersionBase):
    dataset_version_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
