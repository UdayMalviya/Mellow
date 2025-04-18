# api/routers/log.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from configurations.dependencies import get_db
from backend.databases.schemas.log import LogCreate, LogOut
from backend.databases.crud import crud_log

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.post("/", response_model=LogOut)
def create_log(log_in: LogCreate, db: Session = Depends(get_db)):
    return crud_log.create_log(db, log_in)

@router.get("/", response_model=List[LogOut])
def list_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_log.get_all_logs(db, skip, limit)

@router.get("/user/{user_id}", response_model=List[LogOut])
def get_user_logs(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_log.get_logs_by_user(db, user_id, skip, limit)

@router.get("/level/{level}", response_model=List[LogOut])
def get_logs_by_level(level: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_log.get_logs_by_level(db, level, skip, limit)

@router.delete("/cleanup/", response_model=bool)
def delete_old_logs(before: datetime = Query(...), db: Session = Depends(get_db)):
    crud_log.delete_old_logs(db, before)
    return True
