from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PermissionBase(BaseModel):
    sector_id: int
    resource: str
    action: str

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserPermission(BaseModel):
    id: int
    user_id: int
    permission_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
