# crud/crud_timeseries_metadata.py
from sqlalchemy.orm import Session
from backend.databases.models import TimeSeriesMetadata
from backend.databases.schemas.time_series_meta import (
    TimeSeriesMetadataCreate,
    TimeSeriesMetadataUpdate
)

def create_metadata(db: Session, metadata_in: TimeSeriesMetadataCreate):
    db_obj = TimeSeriesMetadata(**metadata_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_metadata(db: Session, timeseries_id: int):
    return db.query(TimeSeriesMetadata).filter(TimeSeriesMetadata.timeseries_id == timeseries_id).first()

def get_metadata_by_source(db: Session, source_id: int):
    return db.query(TimeSeriesMetadata).filter(TimeSeriesMetadata.source_id == source_id).all()

def update_metadata(db: Session, timeseries_id: int, metadata_update: TimeSeriesMetadataUpdate):
    db_obj = db.query(TimeSeriesMetadata).filter(TimeSeriesMetadata.timeseries_id == timeseries_id).first()
    if not db_obj:
        return None
    for key, value in metadata_update.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_metadata(db: Session, timeseries_id: int):
    db_obj = db.query(TimeSeriesMetadata).filter(TimeSeriesMetadata.timeseries_id == timeseries_id).first()
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True
