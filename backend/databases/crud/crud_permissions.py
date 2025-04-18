from sqlalchemy.orm import Session
from backend.databases.models import Permission
from backend.databases.schemas.permissions import PermissionCreate, PermissionUpdate


def create_permission(db: Session, permission: PermissionCreate) -> Permission:
    db_permission = Permission(**permission.model_dump())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def get_permission(db: Session, permission_id: int) -> Permission | None:
    return db.query(Permission).filter(Permission.permission_id == permission_id).first()


def get_permissions(db: Session, skip: int = 0, limit: int = 100) -> list[Permission]:
    return db.query(Permission).offset(skip).limit(limit).all()


def update_permission(db: Session, permission_id: int, permission_update: PermissionUpdate) -> Permission | None:
    db_permission = db.query(Permission).filter(Permission.permission_id == permission_id).first()
    if not db_permission:
        return None

    update_data = permission_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_permission, key, value)

    db.commit()
    db.refresh(db_permission)
    return db_permission


def delete_permission(db: Session, permission_id: int) -> bool:
    db_permission = db.query(Permission).filter(Permission.permission_id == permission_id).first()
    if not db_permission:
        return False

    db.delete(db_permission)
    db.commit()
    return True
