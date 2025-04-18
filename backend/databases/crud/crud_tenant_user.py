# crud/crud_tenant_user.py
from sqlalchemy.orm import Session
from backend.databases.models import TenantUser
from backend.databases.schemas.tenant_user import TenantUserCreate

def create_tenant_user(db: Session, tenant_user_data: TenantUserCreate):
    db_entry = TenantUser(**tenant_user_data.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_users_by_tenant(db: Session, tenant_id: int):
    return db.query(TenantUser).filter(TenantUser.tenant_id == tenant_id).all()

def get_tenants_by_user(db: Session, user_id: int):
    return db.query(TenantUser).filter(TenantUser.user_id == user_id).all()

def delete_tenant_user(db: Session, tenant_id: int, user_id: int):
    entry = db.query(TenantUser).filter_by(tenant_id=tenant_id, user_id=user_id).first()
    if entry:
        db.delete(entry)
        db.commit()
        return True
    return False
