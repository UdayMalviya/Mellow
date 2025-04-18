# api/routers/dataset.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.databases.crud import crud_dataset
from backend.databases.schemas.dataset import DatasetCreate, DatasetUpdate, DatasetOut
from configurations.dependencies import get_db  # Adjust path accordingly

router = APIRouter(prefix="/datasets", tags=["Datasets"])

@router.post("/", response_model=DatasetOut)
def create_dataset(dataset_in: DatasetCreate, db: Session = Depends(get_db)):
    return crud_dataset.create_dataset(db, dataset_in)

@router.get("/{dataset_id}", response_model=DatasetOut)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = crud_dataset.get_dataset(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

@router.get("/tenant/{tenant_id}", response_model=list[DatasetOut])
def get_by_tenant(tenant_id: int, db: Session = Depends(get_db)):
    return crud_dataset.get_datasets_by_tenant(db, tenant_id)

@router.put("/{dataset_id}", response_model=DatasetOut)
def update_dataset(dataset_id: int, dataset_update: DatasetUpdate, db: Session = Depends(get_db)):
    dataset = crud_dataset.update_dataset(db, dataset_id, dataset_update)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

@router.delete("/{dataset_id}", response_model=bool)
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    success = crud_dataset.delete_dataset(db, dataset_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return success
