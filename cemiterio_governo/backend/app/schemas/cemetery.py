from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CemeteryBase(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    area_m2: Optional[float] = None
    description: Optional[str] = None

class CemeteryCreate(CemeteryBase):
    pass

class CemeteryUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    area_m2: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class Cemetery(CemeteryBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
