# crud/crud_metric.py
from sqlalchemy.orm import Session
from backend.databases.models import Metric
from backend.databases.schemas.metric import MetricCreate
from typing import List
from datetime import datetime

def create_metric(db: Session, metric_in: MetricCreate):
    db_obj = Metric(**metric_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_metrics_by_name(db: Session, name: str, skip: int = 0, limit: int = 100) -> List[Metric]:
    return db.query(Metric).filter(Metric.metric_name == name).offset(skip).limit(limit).all()

def get_all_metrics(db: Session, skip: int = 0, limit: int = 100) -> List[Metric]:
    return db.query(Metric).order_by(Metric.timestamp.desc()).offset(skip).limit(limit).all()

def delete_old_metrics(db: Session, before_date: datetime):
    db.query(Metric).filter(Metric.timestamp < before_date).delete()
    db.commit()
