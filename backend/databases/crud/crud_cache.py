# crud/crud_cache.py
from sqlalchemy.orm import Session
from backend.databases.models import Cache
from backend.databases.schemas.cache import CacheCreate, CacheUpdate
from datetime import datetime

def create_cache(db: Session, cache_in: CacheCreate):
    db_obj = Cache(**cache_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_cache_by_key(db: Session, cache_key: str):
    cache = db.query(Cache).filter(Cache.cache_key == cache_key).first()
    if cache and cache.expires_at > datetime.now():
        return cache
    return None  # expired or not found

def update_cache(db: Session, cache_key: str, cache_update: CacheUpdate):
    db_obj = db.query(Cache).filter(Cache.cache_key == cache_key).first()
    if not db_obj:
        return None
    for key, value in cache_update.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_cache(db: Session, cache_key: str):
    db_obj = db.query(Cache).filter(Cache.cache_key == cache_key).first()
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True

def clear_expired_cache(db: Session):
    db.query(Cache).filter(Cache.expires_at < datetime.now()).delete()
    db.commit()
