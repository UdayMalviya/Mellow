from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
# from backend.databases import crud, models, schemas
from backend.databases.crud import crud_user
from backend.databases.schemas import users
# from backend.databases import models
from configurations.dependencies import engine, get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"])
# Route to create a new user
@router.post("/", response_model=users.UserOut)
def create_user(user: users.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.create_user(db=db, user=user)
    return db_user

# Route to get a user by ID
@router.get("/{user_id}", response_model=users.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Route to get all users
@router.get("/", response_model=List[users.UserOut])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = crud_user.get_users(db=db, skip=skip, limit=limit)
    return db_users

# Route to update user details
@router.put("/{user_id}", response_model=users.UserOut)
def update_user(user_id: int, user: users.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Route to delete a user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud_user.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

