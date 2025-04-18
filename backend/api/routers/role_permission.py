# routers/role_permission.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.databases.schemas.role_permission import RolePermissionCreate
from backend.databases.crud import role_permission
from configurations.dependencies import get_db

router = APIRouter(prefix="/role-permissions", tags=["Role-Permissions"])

@router.post("/", status_code=201)
def assign_permission(payload: RolePermissionCreate, db: Session = Depends(get_db)):
    return role_permission.assign_permission_to_role(db, payload.role_id, payload.permission_id)

@router.delete("/", status_code=204)
def remove_permission(payload: RolePermissionCreate, db: Session = Depends(get_db)):
    success = role_permission.remove_permission_from_role(db, payload.role_id, payload.permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mapping not found")
