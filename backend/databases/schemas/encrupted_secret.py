# schemas/encrypted_secret.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class EncryptedSecretBase(BaseModel):
    tenant_id: int
    secret_key: str
    secret_value: str

class EncryptedSecretCreate(EncryptedSecretBase):
    pass

class EncryptedSecretUpdate(BaseModel):
    secret_key: Optional[str] = None
    secret_value: Optional[str] = None

class EncryptedSecretOut(EncryptedSecretBase):
    secret_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
