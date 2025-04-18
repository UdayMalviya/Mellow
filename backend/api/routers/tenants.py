from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from configurations.dependencies import get_db
from backend.databases.schemas.tenant import TenantCreate, TenantUpdate, TenantRead
from backend.databases.crud import crud_tenant

router = APIRouter(prefix="/tenants", tags=["Tenants"])

# Create a new tenant
@router.post("/", response_model=TenantRead)
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    try:
        return crud_tenant.create_tenant(db=db, tenant_data=tenant)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get a single tenant by ID
@router.get("/{tenant_id}", response_model=TenantRead)
def read_tenant(tenant_id: int, db: Session = Depends(get_db)):
    db_tenant = crud_tenant.get_tenant_by_id(db, tenant_id)
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant

# Get all tenants
@router.get("/", response_model=List[TenantRead])
def read_tenants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_tenant.get_tenants(db, skip=skip, limit=limit)

# Update a tenant
@router.put("/{tenant_id}", response_model=TenantRead)
def update_tenant(tenant_id: int, tenant: TenantUpdate, db: Session = Depends(get_db)):
    db_tenant = crud_tenant.update_tenant(db=db, tenant_id=tenant_id, tenant_data=tenant)
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant

# Delete a tenant
@router.delete("/{tenant_id}")
def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    success = crud_tenant.delete_tenant(db, tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {"detail": "Tenant deleted successfully"}
