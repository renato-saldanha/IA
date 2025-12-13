from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.models.permission import Permission, UserPermission
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    token_data = TokenData(email=email)
    
    result = await db.execute(
        select(User).where(
            User.email == token_data.email,
            User.is_active == True,
            User.deleted_at.is_(None)
        )
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user

async def check_permission(
    resource: str,
    action: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> bool:
    """Check if user has permission for a resource and action"""
    # Admin users have all permissions
    if current_user.email == "admin@cemiterio.gov.br":
        return True
    
    # Check user permissions
    result = await db.execute(
        select(Permission)
        .join(UserPermission, Permission.id == UserPermission.permission_id)
        .where(
            UserPermission.user_id == current_user.id,
            Permission.resource == resource,
            Permission.action == action,
            Permission.is_active == True,
            Permission.deleted_at.is_(None),
            UserPermission.is_active == True
        )
    )
    permission = result.scalar_one_or_none()
    
    if permission is None:
        # Check sector permissions
        if current_user.sector_id:
            result = await db.execute(
                select(Permission).where(
                    Permission.sector_id == current_user.sector_id,
                    Permission.resource == resource,
                    Permission.action == action,
                    Permission.is_active == True,
                    Permission.deleted_at.is_(None)
                )
            )
            permission = result.scalar_one_or_none()
    
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied: {action} on {resource}"
        )
    
    return True

def get_permission_dependency(resource: str, action: str):
    """Create a permission dependency"""
    return Depends(lambda: check_permission(resource, action))
