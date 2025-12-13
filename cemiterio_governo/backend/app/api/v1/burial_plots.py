from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.database import get_db
from app.core.logging import log_audit
from app.api.dependencies import get_current_user, check_permission
from app.models.burial_plot import BurialPlot
from app.models.cemetery import Cemetery
from app.schemas.burial_plot import BurialPlot as BurialPlotSchema, BurialPlotCreate, BurialPlotUpdate

router = APIRouter()

@router.get("/", response_model=List[BurialPlotSchema])
async def read_burial_plots(
    skip: int = 0,
    limit: int = 100,
    cemetery_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of burial plots"""
    await check_permission("burial_plots", "read", current_user, db)
    
    query = select(BurialPlot).where(BurialPlot.deleted_at.is_(None))
    
    if cemetery_id:
        query = query.where(BurialPlot.cemetery_id == cemetery_id)
    if status:
        query = query.where(BurialPlot.status == status)
    
    result = await db.execute(query.offset(skip).limit(limit))
    burial_plots = result.scalars().all()
    return burial_plots

@router.get("/{plot_id}", response_model=BurialPlotSchema)
async def read_burial_plot(
    plot_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific burial plot"""
    await check_permission("burial_plots", "read", current_user, db)
    
    result = await db.execute(
        select(BurialPlot).where(BurialPlot.id == plot_id, BurialPlot.deleted_at.is_(None))
    )
    plot = result.scalar_one_or_none()
    
    if not plot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Burial plot not found"
        )
    
    return plot

@router.post("/", response_model=BurialPlotSchema, status_code=status.HTTP_201_CREATED)
async def create_burial_plot(
    plot: BurialPlotCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new burial plot"""
    await check_permission("burial_plots", "create", current_user, db)
    
    # Verify cemetery exists
    result = await db.execute(
        select(Cemetery).where(Cemetery.id == plot.cemetery_id, Cemetery.deleted_at.is_(None))
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cemetery not found"
        )
    
    db_plot = BurialPlot(**plot.model_dump())
    db.add(db_plot)
    await db.commit()
    await db.refresh(db_plot)
    
    # Log creation
    await log_audit(
        db,
        user_id=current_user.id,
        action="create",
        entity_type="burial_plot",
        entity_id=db_plot.id,
        details=plot.model_dump()
    )
    
    return db_plot

@router.put("/{plot_id}", response_model=BurialPlotSchema)
async def update_burial_plot(
    plot_id: int,
    plot_update: BurialPlotUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a burial plot"""
    await check_permission("burial_plots", "update", current_user, db)
    
    result = await db.execute(
        select(BurialPlot).where(BurialPlot.id == plot_id, BurialPlot.deleted_at.is_(None))
    )
    db_plot = result.scalar_one_or_none()
    
    if not db_plot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Burial plot not found"
        )
    
    update_data = plot_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_plot, field, value)
    
    await db.commit()
    await db.refresh(db_plot)
    
    # Log update
    await log_audit(
        db,
        user_id=current_user.id,
        action="update",
        entity_type="burial_plot",
        entity_id=db_plot.id,
        details=update_data
    )
    
    return db_plot

@router.delete("/{plot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_burial_plot(
    plot_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a burial plot (logical deletion)"""
    await check_permission("burial_plots", "delete", current_user, db)
    
    result = await db.execute(
        select(BurialPlot).where(BurialPlot.id == plot_id, BurialPlot.deleted_at.is_(None))
    )
    db_plot = result.scalar_one_or_none()
    
    if not db_plot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Burial plot not found"
        )
    
    from datetime import datetime
    db_plot.deleted_at = datetime.utcnow()
    await db.commit()
    
    # Log deletion
    await log_audit(
        db,
        user_id=current_user.id,
        action="delete",
        entity_type="burial_plot",
        entity_id=db_plot.id
    )
