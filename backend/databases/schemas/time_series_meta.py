# schemas/time_series_metadata.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TimeSeriesMetadataBase(BaseModel):
    source_id: int
    timeseries_name: str
    description: Optional[str] = None

class TimeSeriesMetadataCreate(TimeSeriesMetadataBase):
    pass

class TimeSeriesMetadataUpdate(BaseModel):
    timeseries_name: Optional[str] = None
    description: Optional[str] = None

class TimeSeriesMetadataOut(TimeSeriesMetadataBase):
    timeseries_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
