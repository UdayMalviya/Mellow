# api/router.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to Mellow BI Platform"}
