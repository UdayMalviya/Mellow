# routes/user_roles.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.databases.crud.crud_user_role import assign_role_to_user, remove_role_from_user
from backend.databases.schemas.user_role import UserRoleCreate, UserRoleRead
from configurations.dependencies import get_db  # Ensure this import gives you a session

router = APIRouter(prefix="/user-roles", tags=["User-Roles"])
# router = APIRouter(prefix="/role-permissions", tags=["Role-Permissions"])

@router.post("/assign_role/", response_model=UserRoleRead)
def assign_role(user_role: UserRoleCreate, db: Session = Depends(get_db)):
    # Assign a role to a user using the UserRoleCreate schema
    role = assign_role_to_user(db=db, user_id=user_role.user_id, role_id=user_role.role_id)
    if not role:
        raise HTTPException(status_code=400, detail="Role assignment failed")
    return role

@router.post("/remove_role/", response_model=UserRoleRead)
def remove_role(user_role: UserRoleCreate, db: Session = Depends(get_db)):
    # Remove a role from a user
    success = remove_role_from_user(db=db, user_id=user_role.user_id, role_id=user_role.role_id)
    if not success:
        raise HTTPException(status_code=400, detail="Role removal failed")
    return {"user_id": user_role.user_id, "role_id": user_role.role_id}
