from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.databases.schemas.permissions import PermissionCreate, PermissionRead, PermissionUpdate
from backend.databases.crud import crud_permissions
from configurations.dependencies import get_db

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post("/", response_model=PermissionRead, status_code=status.HTTP_201_CREATED)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    db_permission = crud_permissions.create_permission(db, permission)
    return db_permission


@router.get("/", response_model=list[PermissionRead])
def read_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_permissions.get_permissions(db, skip=skip, limit=limit)


@router.get("/{permission_id}", response_model=PermissionRead)
def read_permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = crud_permissions.get_permission(db, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission


@router.put("/{permission_id}", response_model=PermissionRead)
def update_permission(permission_id: int, permission: PermissionUpdate, db: Session = Depends(get_db)):
    db_permission = crud_permissions.update_permission(db, permission_id, permission)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    success = crud_permissions.delete_permission(db, permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return
