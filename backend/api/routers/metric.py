# api/routers/metric.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from configurations.dependencies import get_db
from backend.databases.schemas.metric import MetricCreate, MetricOut
from backend.databases.crud import crud_metric

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.post("/", response_model=MetricOut)
def create_metric(metric_in: MetricCreate, db: Session = Depends(get_db)):
    return crud_metric.create_metric(db, metric_in)

@router.get("/", response_model=List[MetricOut])
def list_metrics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_metric.get_all_metrics(db, skip, limit)

@router.get("/name/{metric_name}", response_model=List[MetricOut])
def get_by_name(metric_name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_metric.get_metrics_by_name(db, metric_name, skip, limit)

@router.delete("/cleanup/", response_model=bool)
def delete_old(before: datetime = Query(...), db: Session = Depends(get_db)):
    crud_metric.delete_old_metrics(db, before)
    return True
