# crud/crud_log.py
from sqlalchemy.orm import Session
from backend.databases.models import Log
from backend.databases.schemas.log import LogCreate
from typing import List
from datetime import datetime

def create_log(db: Session, log_in: LogCreate):
    db_log = Log(**log_in.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Log]:
    return db.query(Log).filter(Log.user_id == user_id).order_by(Log.timestamp.desc()).offset(skip).limit(limit).all()

def get_logs_by_level(db: Session, level: str, skip: int = 0, limit: int = 100) -> List[Log]:
    return db.query(Log).filter(Log.log_level == level).order_by(Log.timestamp.desc()).offset(skip).limit(limit).all()

def get_all_logs(db: Session, skip: int = 0, limit: int = 100) -> List[Log]:
    return db.query(Log).order_by(Log.timestamp.desc()).offset(skip).limit(limit).all()

def delete_old_logs(db: Session, before_date: datetime):
    db.query(Log).filter(Log.timestamp < before_date).delete()
    db.commit()
