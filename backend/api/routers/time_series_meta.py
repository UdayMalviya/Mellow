# api/routers/time_series_metadata.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.databases.schemas.time_series_meta import (
    TimeSeriesMetadataCreate,
    TimeSeriesMetadataUpdate,
    TimeSeriesMetadataOut
)
from backend.databases.crud import time_series_meta
from configurations.dependencies import get_db  # Adjust path

router = APIRouter(prefix="/time-series", tags=["Time Series Metadata"])

@router.post("/", response_model=TimeSeriesMetadataOut)
def create(metadata_in: TimeSeriesMetadataCreate, db: Session = Depends(get_db)):
    return time_series_meta.create_metadata(db, metadata_in)

@router.get("/{timeseries_id}", response_model=TimeSeriesMetadataOut)
def read(timeseries_id: int, db: Session = Depends(get_db)):
    metadata = time_series_meta.get_metadata(db, timeseries_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="Time series metadata not found")
    return metadata

@router.get("/source/{source_id}", response_model=list[TimeSeriesMetadataOut])
def list_by_source(source_id: int, db: Session = Depends(get_db)):
    return time_series_meta.get_metadata_by_source(db, source_id)

@router.put("/{timeseries_id}", response_model=TimeSeriesMetadataOut)
def update(timeseries_id: int, metadata_update: TimeSeriesMetadataUpdate, db: Session = Depends(get_db)):
    metadata = time_series_meta.update_metadata(db, timeseries_id, metadata_update)
    if not metadata:
        raise HTTPException(status_code=404, detail="Time series metadata not found")
    return metadata

@router.delete("/{timeseries_id}", response_model=bool)
def delete(timeseries_id: int, db: Session = Depends(get_db)):
    success = time_series_meta.delete_metadata(db, timeseries_id)
    if not success:
        raise HTTPException(status_code=404, detail="Time series metadata not found")
    return success
