# crud/crud_encrypted_secret.py
from sqlalchemy.orm import Session
from backend.databases.models import EncryptedSecret
from backend.databases.schemas.encrupted_secret import EncryptedSecretCreate, EncryptedSecretUpdate

def create_secret(db: Session, secret_in: EncryptedSecretCreate):
    db_obj = EncryptedSecret(**secret_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_secret_by_id(db: Session, secret_id: int):
    return db.query(EncryptedSecret).filter(EncryptedSecret.secret_id == secret_id).first()

def get_secrets_by_tenant(db: Session, tenant_id: int):
    return db.query(EncryptedSecret).filter(EncryptedSecret.tenant_id == tenant_id).all()

def update_secret(db: Session, secret_id: int, secret_update: EncryptedSecretUpdate):
    db_obj = db.query(EncryptedSecret).filter(EncryptedSecret.secret_id == secret_id).first()
    if not db_obj:
        return None
    for key, value in secret_update.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_secret(db: Session, secret_id: int):
    db_obj = db.query(EncryptedSecret).filter(EncryptedSecret.secret_id == secret_id).first()
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True
