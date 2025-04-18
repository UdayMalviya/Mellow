# crud/crud_process_tracking.py
from sqlalchemy.orm import Session
from backend.databases.models import ProcessTracking
from backend.databases.schemas.process_tracking import ProcessTrackingCreate, ProcessTrackingUpdate
from typing import List, Optional

def create_process(db: Session, process_in: ProcessTrackingCreate) -> ProcessTracking:
    db_process = ProcessTracking(**process_in.model_dump())
    db.add(db_process)
    db.commit()
    db.refresh(db_process)
    return db_process

def get_process(db: Session, process_id: int) -> Optional[ProcessTracking]:
    return db.query(ProcessTracking).filter(ProcessTracking.process_id == process_id).first()

def get_all_processes(db: Session, skip: int = 0, limit: int = 100) -> List[ProcessTracking]:
    return db.query(ProcessTracking).order_by(ProcessTracking.created_at.desc()).offset(skip).limit(limit).all()

def update_process(db: Session, process_id: int, process_update: ProcessTrackingUpdate) -> Optional[ProcessTracking]:
    process = get_process(db, process_id)
    if not process:
        return None
    for key, value in process_update.model_dump(exclude_unset=True).items():
        setattr(process, key, value)
    db.commit()
    db.refresh(process)
    return process

def get_processes_by_status(db: Session, status: str) -> List[ProcessTracking]:
    return db.query(ProcessTracking).filter(ProcessTracking.status == status).all()
