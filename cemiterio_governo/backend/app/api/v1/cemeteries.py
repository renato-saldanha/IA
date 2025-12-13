from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.logging import log_audit
from app.api.dependencies import get_current_user, check_permission
from app.models.cemetery import Cemetery
from app.schemas.cemetery import Cemetery as CemeterySchema, CemeteryCreate, CemeteryUpdate

router = APIRouter()

@router.get("/", response_model=List[CemeterySchema])
async def read_cemeteries(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of cemeteries"""
    await check_permission("cemeteries", "read", current_user, db)
    
    result = await db.execute(
        select(Cemetery)
        .where(Cemetery.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    cemeteries = result.scalars().all()
    return cemeteries

@router.get("/{cemetery_id}", response_model=CemeterySchema)
async def read_cemetery(
    cemetery_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific cemetery"""
    await check_permission("cemeteries", "read", current_user, db)
    
    result = await db.execute(
        select(Cemetery).where(Cemetery.id == cemetery_id, Cemetery.deleted_at.is_(None))
    )
    cemetery = result.scalar_one_or_none()
    
    if not cemetery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cemetery not found"
        )
    
    return cemetery

@router.post("/", response_model=CemeterySchema, status_code=status.HTTP_201_CREATED)
async def create_cemetery(
    cemetery: CemeteryCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new cemetery"""
    await check_permission("cemeteries", "create", current_user, db)
    
    db_cemetery = Cemetery(**cemetery.model_dump())
    db.add(db_cemetery)
    await db.commit()
    await db.refresh(db_cemetery)
    
    # Log creation
    await log_audit(
        db,
        user_id=current_user.id,
        action="create",
        entity_type="cemetery",
        entity_id=db_cemetery.id,
        details=cemetery.model_dump()
    )
    
    return db_cemetery

@router.put("/{cemetery_id}", response_model=CemeterySchema)
async def update_cemetery(
    cemetery_id: int,
    cemetery_update: CemeteryUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a cemetery"""
    await check_permission("cemeteries", "update", current_user, db)
    
    result = await db.execute(
        select(Cemetery).where(Cemetery.id == cemetery_id, Cemetery.deleted_at.is_(None))
    )
    db_cemetery = result.scalar_one_or_none()
    
    if not db_cemetery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cemetery not found"
        )
    
    update_data = cemetery_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cemetery, field, value)
    
    await db.commit()
    await db.refresh(db_cemetery)
    
    # Log update
    await log_audit(
        db,
        user_id=current_user.id,
        action="update",
        entity_type="cemetery",
        entity_id=db_cemetery.id,
        details=update_data
    )
    
    return db_cemetery

@router.delete("/{cemetery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cemetery(
    cemetery_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a cemetery (logical deletion)"""
    await check_permission("cemeteries", "delete", current_user, db)
    
    result = await db.execute(
        select(Cemetery).where(Cemetery.id == cemetery_id, Cemetery.deleted_at.is_(None))
    )
    db_cemetery = result.scalar_one_or_none()
    
    if not db_cemetery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cemetery not found"
        )
    
    from datetime import datetime
    db_cemetery.deleted_at = datetime.utcnow()
    await db.commit()
    
    # Log deletion
    await log_audit(
        db,
        user_id=current_user.id,
        action="delete",
        entity_type="cemetery",
        entity_id=db_cemetery.id
    )
