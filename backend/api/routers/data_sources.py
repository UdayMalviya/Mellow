# api/routers/data_sources.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.databases.schemas.data_source import DataSourceCreate, DataSourceOut, DataSourceUpdate
from backend.databases.crud import data_source
from configurations.dependencies import get_db  # Adjust path

router = APIRouter(prefix="/data-sources", tags=["Data Sources"])

@router.post("/", response_model=DataSourceOut)
def create_source(ds: DataSourceCreate, db: Session = Depends(get_db)):
    return data_source.create_data_source(db, ds)

@router.get("/{source_id}", response_model=DataSourceOut)
def get_source(source_id: int, db: Session = Depends(get_db)):
    ds = data_source.get_data_source(db, source_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Data source not found")
    return ds

@router.get("/tenant/{tenant_id}", response_model=list[DataSourceOut])
def list_sources(tenant_id: int, db: Session = Depends(get_db)):
    return data_source.get_all_data_sources(db, tenant_id)

@router.put("/{source_id}", response_model=DataSourceOut)
def update_source(source_id: int, ds_update: DataSourceUpdate, db: Session = Depends(get_db)):
    ds = data_source.update_data_source(db, source_id, ds_update)
    if not ds:
        raise HTTPException(status_code=404, detail="Data source not found")
    return ds

@router.delete("/{source_id}", response_model=bool)
def delete_source(source_id: int, db: Session = Depends(get_db)):
    success = data_source.delete_data_source(db, source_id)
    if not success:
        raise HTTPException(status_code=404, detail="Data source not found")
    return success
