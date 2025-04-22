from sqlalchemy.orm import Session
from backend.db import models
from backend.db.schemas import schema

def create_dataset(db: Session, dataset: schema.DatasetCreate):
    db_dataset = models.Dataset(**dataset.model_dump())
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

def get_dataset(db: Session, dataset_id: int):
    return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()

def get_all_datasets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dataset).offset(skip).limit(limit).all()
