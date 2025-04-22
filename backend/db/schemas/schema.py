from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class DatasetVersionBase(BaseModel):
    version: str
    status: Optional[str]
    file_path: Optional[str]
    preprocessing_summary: Optional[dict]
    num_rows: Optional[int]
    num_columns: Optional[int]

class DatasetVersionCreate(DatasetVersionBase):
    pass

class DatasetVersion(DatasetVersionBase):
    id: int
    dataset_id: int
    file_path: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DatasetBase(BaseModel):
    name: str
    description: Optional[str]
    created_by: str

class DatasetCreate(DatasetBase):
    pass

class Dataset(DatasetBase):
    id: int
    created_at: datetime
    versions: List[DatasetVersion] = []

    model_config = ConfigDict(from_attributes=True)
