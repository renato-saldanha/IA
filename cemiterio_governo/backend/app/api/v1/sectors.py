from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.logging import log_audit
from app.api.dependencies import get_current_user, check_permission
from app.models.sector import Sector
from app.schemas.sector import Sector as SectorSchema, SectorCreate, SectorUpdate

router = APIRouter()

@router.get("/", response_model=List[SectorSchema])
async def read_sectors(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of sectors"""
    await check_permission("sectors", "read", current_user, db)
    
    result = await db.execute(
        select(Sector)
        .where(Sector.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    sectors = result.scalars().all()
    return sectors

@router.post("/", response_model=SectorSchema, status_code=status.HTTP_201_CREATED)
async def create_sector(
    sector: SectorCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new sector"""
    await check_permission("sectors", "create", current_user, db)
    
    db_sector = Sector(**sector.model_dump())
    db.add(db_sector)
    await db.commit()
    await db.refresh(db_sector)
    
    await log_audit(
        db,
        user_id=current_user.id,
        action="create",
        entity_type="sector",
        entity_id=db_sector.id,
        details=sector.model_dump()
    )
    
    return db_sector

@router.put("/{sector_id}", response_model=SectorSchema)
async def update_sector(
    sector_id: int,
    sector_update: SectorUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a sector"""
    await check_permission("sectors", "update", current_user, db)
    
    result = await db.execute(
        select(Sector).where(Sector.id == sector_id, Sector.deleted_at.is_(None))
    )
    db_sector = result.scalar_one_or_none()
    
    if not db_sector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sector not found"
        )
    
    update_data = sector_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sector, field, value)
    
    await db.commit()
    await db.refresh(db_sector)
    
    await log_audit(
        db,
        user_id=current_user.id,
        action="update",
        entity_type="sector",
        entity_id=db_sector.id,
        details=update_data
    )
    
    return db_sector
