# schemas/metric.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MetricBase(BaseModel):
    metric_name: str
    metric_value: str
    timestamp: datetime

class MetricCreate(MetricBase):
    pass

class MetricOut(MetricBase):
    metric_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
