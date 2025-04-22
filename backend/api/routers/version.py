import os
import json
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.db.crud import version as crud_version
from backend.db.schemas import schema
from backend.db.session import get_db

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/versions", tags=["versions"])

# POST with FormData + File Upload
@router.post("/{dataset_id}", response_model=schema.DatasetVersion)
def add_version(
    dataset_id: int,
    version: str = Form(...),
    status: str = Form(...),
    preprocessing_summary: str = Form(...),
    num_rows: int = Form(...),
    num_columns: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Validate and parse preprocessing_summary
    try:
        summary_dict = json.loads(preprocessing_summary)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in preprocessing_summary")

    # Save file to disk
    filename = f"{dataset_id}_{version}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Wrap into schema and delegate to CRUD
    version_data = schema.DatasetVersionCreate(
        version=version,
        status=status,
        file_path=file_path,
        preprocessing_summary=summary_dict,
        num_rows=num_rows,
        num_columns=num_columns,
    )

    return crud_version.create_version(db, dataset_id, version_data)


# GET all versions for a dataset
@router.get("/{dataset_id}", response_model=list[schema.DatasetVersion])
def list_versions(dataset_id: int, db: Session = Depends(get_db)):
    return crud_version.get_versions_by_dataset(db, dataset_id)


# GET a single version by version ID (optional but useful)
@router.get("/detail/{version_id}", response_model=schema.DatasetVersion)
def get_version(version_id: int, db: Session = Depends(get_db)):
    version = crud_version.get_version(db, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    return version


# GET file download endpoint
@router.get("/file/{filename}")
def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
