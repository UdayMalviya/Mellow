import os
from fastapi import UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from backend.db import models
from backend.db.schemas import schema
from datetime import datetime
from pathlib import Path
import pandas as pd

UPLOAD_DIR = "uploaded_files"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def read_file(file_path: str) -> pd.DataFrame:
    ext = Path(file_path).suffix.lower()
    if ext == ".csv":
        return pd.read_csv(file_path)
    elif ext in [".xls", ".xlsx"]:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def create_version(db: Session,
                   dataset_id: int,
                   version_data: schema.DatasetVersionCreate,
                   file: UploadFile = None):
    file_path = None
    if file:
        file_path = os.path.join(UPLOAD_DIR, f"{dataset_id}_{version_data.version}_{file.filename}")
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        try:
            df = read_file(file_path)
            if df.empty:
                raise ValueError("File is empty")

            num_rows, num_columns = df.shape

            summary = {
                "columns":df.columns.tolist(),
                "num_rows": num_rows,
                "num_columns": num_columns
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"File preprocessing error:{str(e)}")


    db_version = models.DatasetVersion(**version_data.model_dump(), dataset_id=dataset_id)
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version

def get_versions_by_dataset(db: Session, dataset_id: int):
    return db.query(models.DatasetVersion).filter(models.DatasetVersion.dataset_id == dataset_id).all()

def get_version(db: Session, version_id: int):
    # Query the database to get a version by its ID
    return db.query(models.DatasetVersion).filter(models.DatasetVersion.id == version_id).first()
