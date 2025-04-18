# crud/crud_data_source.py
from sqlalchemy.orm import Session
from backend.databases.models import DataSource
from backend.databases.schemas.data_source import DataSourceCreate, DataSourceUpdate

def create_data_source(db: Session, ds_in: DataSourceCreate):
    db_ds = DataSource(**ds_in.model_dump())
    db.add(db_ds)
    db.commit()
    db.refresh(db_ds)
    return db_ds

def get_data_source(db: Session, source_id: int):
    return db.query(DataSource).filter(DataSource.source_id == source_id).first()

def get_all_data_sources(db: Session, tenant_id: int):
    return db.query(DataSource).filter(DataSource.tenant_id == tenant_id).all()

def update_data_source(db: Session, source_id: int, ds_update: DataSourceUpdate):
    db_ds = db.query(DataSource).filter(DataSource.source_id == source_id).first()
    if not db_ds:
        return None
    for key, value in ds_update.dict(exclude_unset=True).items():
        setattr(db_ds, key, value)
    db.commit()
    db.refresh(db_ds)
    return db_ds

def delete_data_source(db: Session, source_id: int):
    db_ds = db.query(DataSource).filter(DataSource.source_id == source_id).first()
    if not db_ds:
        return False
    db.delete(db_ds)
    db.commit()
    return True
