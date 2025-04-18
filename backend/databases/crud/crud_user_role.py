# crud/crud_user_role.py
from sqlalchemy.orm import Session
from backend.databases.models import UserRole

# Assign a role to a user
def assign_role_to_user(db: Session, user_id: int, role_id: int):
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role

# Remove a role from a user
def remove_role_from_user(db: Session, user_id: int, role_id: int):
    db_user_role = db.query(UserRole).filter_by(user_id=user_id, role_id=role_id).first()
    if db_user_role:
        db.delete(db_user_role)
        db.commit()
        return True
    return False
