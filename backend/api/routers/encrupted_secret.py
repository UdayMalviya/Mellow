# api/routers/encrypted_secret.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.databases.schemas.encrupted_secret import EncryptedSecretCreate, EncryptedSecretUpdate, EncryptedSecretOut
from backend.databases.crud import crud_encrypted_secret
from configurations.dependencies import get_db  # Assumed dependency

router = APIRouter(prefix="/secrets", tags=["Encrypted Secrets"])

@router.post("/", response_model=EncryptedSecretOut)
def create(secret_in: EncryptedSecretCreate, db: Session = Depends(get_db)):
    return crud_encrypted_secret.create_secret(db, secret_in)

@router.get("/{secret_id}", response_model=EncryptedSecretOut)
def read(secret_id: int, db: Session = Depends(get_db)):
    secret = crud_encrypted_secret.get_secret_by_id(db, secret_id)
    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    return secret

@router.get("/tenant/{tenant_id}", response_model=list[EncryptedSecretOut])
def read_by_tenant(tenant_id: int, db: Session = Depends(get_db)):
    return crud_encrypted_secret.get_secrets_by_tenant(db, tenant_id)

@router.put("/{secret_id}", response_model=EncryptedSecretOut)
def update(secret_id: int, update_in: EncryptedSecretUpdate, db: Session = Depends(get_db)):
    secret = crud_encrypted_secret.update_secret(db, secret_id, update_in)
    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    return secret

@router.delete("/{secret_id}", response_model=bool)
def delete(secret_id: int, db: Session = Depends(get_db)):
    return crud_encrypted_secret.delete_secret(db, secret_id)
