# api/routers/tenant_user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from configurations.dependencies import get_db  # replace with your DB dependency
from backend.databases.schemas.tenant_user import TenantUserCreate, TenantUserOut
# from backend.databases.crud.crud_tenant_user import crud_tenant_user
from backend.databases.crud import crud_tenant_user 

router = APIRouter(prefix="/tenant-user", tags=["TenantUser"])

@router.post("/", response_model=TenantUserOut)
def assign_user_to_tenant(payload: TenantUserCreate, db: Session = Depends(get_db)):
    return crud_tenant_user.create_tenant_user(db, payload)

@router.get("/tenant/{tenant_id}", response_model=list[TenantUserOut])
def get_users(tenant_id: int, db: Session = Depends(get_db)):
    return crud_tenant_user.get_users_by_tenant(db, tenant_id)

@router.get("/user/{user_id}", response_model=list[TenantUserOut])
def get_tenants(user_id: int, db: Session = Depends(get_db)):
    return crud_tenant_user.get_tenants_by_user(db, user_id)

@router.delete("/", response_model=bool)
def unassign_user_from_tenant(payload: TenantUserCreate, db: Session = Depends(get_db)):
    success = crud_tenant_user.delete_tenant_user(db, payload.tenant_id, payload.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Association not found")
    return True
