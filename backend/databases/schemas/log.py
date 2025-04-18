# schemas/log.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class LogBase(BaseModel):
    user_id: int
    log_level: str
    message: str
    timestamp: datetime

class LogCreate(LogBase):
    pass

class LogOut(LogBase):
    log_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
