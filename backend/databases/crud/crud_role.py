from sqlalchemy.orm import Session
from typing import List, Optional
from backend.databases.models import Role
from backend.databases.schemas.roles import RoleCreate, RoleUpdate

# Create a new role
def create_role(db: Session, role: RoleCreate) -> Role:
    db_role = Role(**role.model_dump())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# Get a role by ID
def get_role(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.role_id == role_id).first()

# Get all roles (with pagination)
def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
    return db.query(Role).offset(skip).limit(limit).all()

# Update a role
def update_role(db: Session, role_id: int, role: RoleUpdate) -> Optional[Role]:
    db_role = db.query(Role).filter(Role.role_id == role_id).first()
    if not db_role:
        return None
    for key, value in role.model_dump(exclude_unset=True).items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    return db_role

# Delete a role
def delete_role(db: Session, role_id: int) -> bool:
    db_role = db.query(Role).filter(Role.role_id == role_id).first()
    if not db_role:
        return False
    db.delete(db_role)
    db.commit()
    return True
