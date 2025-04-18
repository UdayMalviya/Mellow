# api/routers/process_tracking.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.databases.schemas.process_tracking import ProcessTrackingCreate, ProcessTrackingOut, ProcessTrackingUpdate
from backend.databases.crud import crud_process_tracking
from configurations.dependencies import get_db
from typing import List

router = APIRouter(prefix="/processes", tags=["Process Tracking"])

@router.post("/", response_model=ProcessTrackingOut)
def create_process_tracking(process_in: ProcessTrackingCreate, db: Session = Depends(get_db)):
    return crud_process_tracking.create_process(db, process_in)

@router.get("/", response_model=List[ProcessTrackingOut])
def list_processes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_process_tracking.get_all_processes(db, skip, limit)

@router.get("/{process_id}", response_model=ProcessTrackingOut)
def get_process(process_id: int, db: Session = Depends(get_db)):
    process = crud_process_tracking.get_process(db, process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")
    return process

@router.put("/{process_id}", response_model=ProcessTrackingOut)
def update_process(process_id: int, update_data: ProcessTrackingUpdate, db: Session = Depends(get_db)):
    updated = crud_process_tracking.update_process(db, process_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Process not found")
    return updated

@router.get("/status/{status}", response_model=List[ProcessTrackingOut])
def get_by_status(status: str, db: Session = Depends(get_db)):
    return crud_process_tracking.get_processes_by_status(db, status)
