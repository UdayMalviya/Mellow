from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from configurations.dependencies import get_db
from backend.databases.crud import crud_role
from backend.databases.schemas.roles import RoleCreate, RoleRead, RoleUpdate


router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

# ✅ Create a new role
@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return crud_role.create_role(db=db, role=role)

# 📥 Get a single role by ID
@router.get("/{role_id}", response_model=RoleRead)
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = crud_role.get_role(db, role_id=role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

# 📜 Get all roles (with pagination)
@router.get("/", response_model=List[RoleRead])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_role.get_roles(db, skip=skip, limit=limit)

# ✏️ Update a role
@router.put("/{role_id}", response_model=RoleRead)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    updated_role = crud_role.update_role(db, role_id=role_id, role=role)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role

# ❌ Delete a role
@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    success = crud_role.delete_role(db, role_id=role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return
