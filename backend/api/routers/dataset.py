from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.crud import dataset as crud_dataset
from backend.db.schemas import schema
from backend.db.session import get_db

router = APIRouter(prefix="/datasets", tags=["datasets"])



@router.post("/", response_model=schema.Dataset)
def create_dataset(dataset: schema.DatasetCreate, db: Session = Depends(get_db)):
    return crud_dataset.create_dataset(db, dataset)

@router.get("/", response_model=list[schema.Dataset])
def list_datasets(db: Session = Depends(get_db)):
    return crud_dataset.get_all_datasets(db)

@router.get("/{dataset_id}", response_model=schema.Dataset)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    db_dataset = crud_dataset.get_dataset(db, dataset_id)
    if not db_dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return db_dataset
