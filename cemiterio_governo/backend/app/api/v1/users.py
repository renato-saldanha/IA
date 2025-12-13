from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.security import get_password_hash
from app.core.logging import log_audit
from app.api.dependencies import get_current_user, check_permission
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.get("/", response_model=List[UserSchema])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of users"""
    await check_permission("users", "read", current_user, db)
    
    result = await db.execute(
        select(User)
        .where(User.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()
    return users

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new user"""
    await check_permission("users", "create", current_user, db)
    
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = User(
        email=user.email,
        password_hash=get_password_hash(user.password),
        full_name=user.full_name,
        sector_id=user.sector_id
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    # Log creation
    await log_audit(
        db,
        user_id=current_user.id,
        action="create",
        entity_type="user",
        entity_id=db_user.id,
        details={"email": user.email, "full_name": user.full_name}
    )
    
    return db_user

@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a user"""
    await check_permission("users", "update", current_user, db)
    
    result = await db.execute(select(User).where(User.id == user_id, User.deleted_at.is_(None)))
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    await db.commit()
    await db.refresh(db_user)
    
    # Log update
    await log_audit(
        db,
        user_id=current_user.id,
        action="update",
        entity_type="user",
        entity_id=db_user.id,
        details=update_data
    )
    
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a user (logical deletion)"""
    await check_permission("users", "delete", current_user, db)
    
    result = await db.execute(select(User).where(User.id == user_id, User.deleted_at.is_(None)))
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    from datetime import datetime
    db_user.deleted_at = datetime.utcnow()
    await db.commit()
    
    # Log deletion
    await log_audit(
        db,
        user_id=current_user.id,
        action="delete",
        entity_type="user",
        entity_id=db_user.id
    )
