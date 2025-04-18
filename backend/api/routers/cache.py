# api/routers/cache.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.databases.schemas.cache import CacheCreate, CacheUpdate, CacheOut
from backend.databases.crud import crud_cache
from configurations.dependencies import get_db

router = APIRouter(prefix="/cache", tags=["Cache"])

@router.post("/", response_model=CacheOut)
def create(cache_in: CacheCreate, db: Session = Depends(get_db)):
    return crud_cache.create_cache(db, cache_in)

@router.get("/{cache_key}", response_model=CacheOut)
def read(cache_key: str, db: Session = Depends(get_db)):
    cache = crud_cache.get_cache_by_key(db, cache_key)
    if not cache:
        raise HTTPException(status_code=404, detail="Cache not found or expired")
    return cache

@router.put("/{cache_key}", response_model=CacheOut)
def update(cache_key: str, update_in: CacheUpdate, db: Session = Depends(get_db)):
    cache = crud_cache.update_cache(db, cache_key, update_in)
    if not cache:
        raise HTTPException(status_code=404, detail="Cache not found")
    return cache

@router.delete("/{cache_key}", response_model=bool)
def delete(cache_key: str, db: Session = Depends(get_db)):
    return crud_cache.delete_cache(db, cache_key)

@router.delete("/expired/", response_model=bool)
def clear_expired(db: Session = Depends(get_db)):
    crud_cache.clear_expired_cache(db)
    return True
