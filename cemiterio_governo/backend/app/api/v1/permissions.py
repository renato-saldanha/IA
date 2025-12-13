from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.logging import log_audit
from app.api.dependencies import get_current_user, check_permission
from app.models.permission import Permission, UserPermission
from app.models.user import User
from app.schemas.permission import Permission as PermissionSchema, PermissionCreate, UserPermission as UserPermissionSchema

router = APIRouter()

@router.get("/", response_model=List[PermissionSchema])
async def read_permissions(
    sector_id: int = None,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of permissions"""
    await check_permission("permissions", "read", current_user, db)
    
    query = select(Permission).where(Permission.deleted_at.is_(None))
    if sector_id:
        query = query.where(Permission.sector_id == sector_id)
    
    result = await db.execute(query)
    permissions = result.scalars().all()
    return permissions

@router.post("/", response_model=PermissionSchema, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission: PermissionCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new permission"""
    await check_permission("permissions", "create", current_user, db)
    
    db_permission = Permission(**permission.model_dump())
    db.add(db_permission)
    await db.commit()
    await db.refresh(db_permission)
    
    await log_audit(
        db,
        user_id=current_user.id,
        action="create",
        entity_type="permission",
        entity_id=db_permission.id,
        details=permission.model_dump()
    )
    
    return db_permission

@router.post("/assign", response_model=UserPermissionSchema, status_code=status.HTTP_201_CREATED)
async def assign_permission_to_user(
    user_id: int,
    permission_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Assign a permission to a user"""
    await check_permission("permissions", "update", current_user, db)
    
    # Verify user exists
    result = await db.execute(select(User).where(User.id == user_id, User.deleted_at.is_(None)))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify permission exists
    result = await db.execute(select(Permission).where(Permission.id == permission_id, Permission.deleted_at.is_(None)))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Permission not found")
    
    # Check if already assigned
    result = await db.execute(
        select(UserPermission).where(
            UserPermission.user_id == user_id,
            UserPermission.permission_id == permission_id
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        existing.is_active = True
        await db.commit()
        await db.refresh(existing)
        return existing
    
    user_permission = UserPermission(user_id=user_id, permission_id=permission_id)
    db.add(user_permission)
    await db.commit()
    await db.refresh(user_permission)
    
    return user_permission
