from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.crud import version as crud_version
from backend.db.session import get_db
from backend.ai.cleaner import clean_with_ai
import os

router = APIRouter(prefix="/versions", tags=["versions"])


@router.post("/{version_id}/clean-with-ai")
def clean_dataset_with_ai(version_id: int, db: Session = Depends(get_db)):
    version = crud_version.get_version_by_id(db, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    file_path = version.file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    try:
        cleaned_df, summary = clean_with_ai(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI cleaning failed: {e}")

    # Save cleaned file
    cleaned_path = file_path.replace(".csv", "_cleaned.csv")
    cleaned_df.to_csv(cleaned_path, index=False)

    # Save as a new version
    new_version = crud_version.create_version_from_cleaned(
        db=db,
        dataset_id=version.dataset_id,
        original_version=version,
        file_path=cleaned_path,
        summary=summary,
        num_rows=cleaned_df.shape[0],
        num_columns=cleaned_df.shape[1]
    )

    return {"message": "Cleaned and saved successfully", "version_id": new_version.id}
