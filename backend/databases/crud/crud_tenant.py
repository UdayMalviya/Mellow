from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from backend.databases.models import Tenant
from backend.databases.schemas.tenant import TenantCreate, TenantUpdate

# Create tenant
def create_tenant(db: Session, tenant_data: TenantCreate) -> Tenant:
    new_tenant = Tenant(**tenant_data.model_dump())
    db.add(new_tenant)
    try:
        db.commit()
        db.refresh(new_tenant)
        return new_tenant
    except IntegrityError:
        db.rollback()
        raise ValueError("Tenant name must be unique.")

# Get tenant by ID
def get_tenant_by_id(db: Session, tenant_id: int) -> Optional[Tenant]:
    return db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()

# Get all tenants
def get_tenants(db: Session, skip: int = 0, limit: int = 100) -> List[Tenant]:
    return db.query(Tenant).offset(skip).limit(limit).all()

# Update tenant
def update_tenant(db: Session, tenant_id: int, tenant_data: TenantUpdate) -> Optional[Tenant]:
    db_tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    if not db_tenant:
        return None

    for field, value in tenant_data.model_dump(exclude_unset=True).items():
        setattr(db_tenant, field, value)

    db.commit()
    db.refresh(db_tenant)
    return db_tenant

# Delete tenant
def delete_tenant(db: Session, tenant_id: int) -> bool:
    db_tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    if not db_tenant:
        return False

    db.delete(db_tenant)
    db.commit()
    return True
