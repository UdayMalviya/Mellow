# api/routers/dataset_version.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.databases.crud import crud_dataset_version
from backend.databases.schemas.dataset_version import DatasetVersionCreate, DatasetVersionUpdate, DatasetVersionOut
from configurations.dependencies import get_db  # adjust if needed

router = APIRouter(prefix="/dataset_versions", tags=["Dataset Versions"])

@router.post("/", response_model=DatasetVersionOut)
def create_version(version_in: DatasetVersionCreate, db: Session = Depends(get_db)):
    return crud_dataset_version.create_dataset_version(db, version_in)

@router.get("/{dataset_version_id}", response_model=DatasetVersionOut)
def get_version(dataset_version_id: int, db: Session = Depends(get_db)):
    version = crud_dataset_version.get_dataset_version(db, dataset_version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    return version

@router.get("/dataset/{dataset_id}", response_model=list[DatasetVersionOut])
def get_versions_for_dataset(dataset_id: int, db: Session = Depends(get_db)):
    return crud_dataset_version.get_versions_by_dataset(db, dataset_id)

@router.put("/{dataset_version_id}", response_model=DatasetVersionOut)
def update_version(dataset_version_id: int, version_update: DatasetVersionUpdate, db: Session = Depends(get_db)):
    version = crud_dataset_version.update_dataset_version(db, dataset_version_id, version_update)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    return version

@router.delete("/{dataset_version_id}", response_model=bool)
def delete_version(dataset_version_id: int, db: Session = Depends(get_db)):
    success = crud_dataset_version.delete_dataset_version(db, dataset_version_id)
    if not success:
        raise HTTPException(status_code=404, detail="Version not found")
    return success
