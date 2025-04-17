from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.databases.models import User, Role
from backend.databases.schemas.users import UserCreate, UserUpdate, UserRead, UserOut
from typing import List
from datetime import datetime

# Create new user
def create_user(db: Session, user: UserCreate) -> UserOut:
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=user.password,  # You should hash the password in real use!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserOut.model_validate(db_user)

# Get user by ID (using UserRead for more detailed info)
def get_user_by_id(db: Session, user_id: int) -> UserRead:
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        return None
    return UserRead.model_validate(db_user)

# Get all users (using UserRead for more detailed info)
def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserRead]:
    db_users = db.query(User).offset(skip).limit(limit).all()
    return [UserRead.model_validate(user) for user in db_users]

# Update user details
def update_user(db: Session, user_id: int, user: UserUpdate) -> UserOut:
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        if user.username:
            db_user.username = user.username
        if user.email:
            db_user.email = user.email
        if user.password:
            db_user.password_hash = user.password  # Hash the password before saving
        db.commit()
        db.refresh(db_user)
        return UserOut.model_validate(db_user)
    return None

# Delete user by ID
def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
