# crud/crud_role_permission.py
from sqlalchemy.orm import Session
from backend.databases.models import RolePermission


def assign_permission_to_role(db: Session, role_id: int, permission_id: int):
    role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
    db.add(role_permission)
    db.commit()
    db.refresh(role_permission)
    return role_permission

def remove_permission_from_role(db: Session, role_id: int, permission_id: int):
    db_role_permission = db.query(RolePermission).filter_by(
        role_id=role_id, permission_id=permission_id
    ).first()
    if db_role_permission:
        db.delete(db_role_permission)
        db.commit()
        return True
    return False
