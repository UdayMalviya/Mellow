# schemas/process_tracking.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ProcessTrackingBase(BaseModel):
    process_name: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[int] = None

class ProcessTrackingCreate(ProcessTrackingBase):
    pass

class ProcessTrackingUpdate(BaseModel):
    status: Optional[str] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None

class ProcessTrackingOut(ProcessTrackingBase):
    process_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
