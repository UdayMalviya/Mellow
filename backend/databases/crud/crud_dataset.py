# crud/crud_dataset.py
from sqlalchemy.orm import Session
from backend.databases.models import Dataset
from backend.databases.schemas.dataset import DatasetCreate, DatasetUpdate

def create_dataset(db: Session, dataset_in: DatasetCreate):
    db_obj = Dataset(**dataset_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_dataset(db: Session, dataset_id: int):
    return db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()

def get_datasets_by_tenant(db: Session, tenant_id: int):
    return db.query(Dataset).filter(Dataset.tenant_id == tenant_id).all()

def update_dataset(db: Session, dataset_id: int, dataset_update: DatasetUpdate):
    db_obj = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
    if not db_obj:
        return None
    for key, value in dataset_update.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_dataset(db: Session, dataset_id: int):
    db_obj = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True
