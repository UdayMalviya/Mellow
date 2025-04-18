# crud/crud_dataset_version.py
from sqlalchemy.orm import Session
from backend.databases.models import DatasetVersion
from backend.databases.schemas.dataset_version import DatasetVersionCreate, DatasetVersionUpdate

def create_dataset_version(db: Session, version_in: DatasetVersionCreate):
    db_obj = DatasetVersion(**version_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_dataset_version(db: Session, dataset_version_id: int):
    return db.query(DatasetVersion).filter(DatasetVersion.dataset_version_id == dataset_version_id).first()

def get_versions_by_dataset(db: Session, dataset_id: int):
    return db.query(DatasetVersion).filter(DatasetVersion.dataset_id == dataset_id).all()

def update_dataset_version(db: Session, dataset_version_id: int, version_update: DatasetVersionUpdate):
    db_obj = db.query(DatasetVersion).filter(DatasetVersion.dataset_version_id == dataset_version_id).first()
    if not db_obj:
        return None
    for key, value in version_update.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_dataset_version(db: Session, dataset_version_id: int):
    db_obj = db.query(DatasetVersion).filter(DatasetVersion.dataset_version_id == dataset_version_id).first()
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True
