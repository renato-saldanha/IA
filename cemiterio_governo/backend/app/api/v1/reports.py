from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any

from app.core.database import get_db
from app.api.dependencies import get_current_user, check_permission
from app.models.cemetery import Cemetery
from app.models.burial_plot import BurialPlot

router = APIRouter()

@router.get("/metrics", response_model=Dict[str, Any])
async def get_metrics(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard metrics"""
    await check_permission("reports", "read", current_user, db)
    
    # Total cemeteries
    result = await db.execute(
        select(func.count(Cemetery.id)).where(Cemetery.deleted_at.is_(None))
    )
    total_cemeteries = result.scalar() or 0
    
    # Total burial plots
    result = await db.execute(
        select(func.count(BurialPlot.id)).where(BurialPlot.deleted_at.is_(None))
    )
    total_plots = result.scalar() or 0
    
    # Available plots
    result = await db.execute(
        select(func.count(BurialPlot.id)).where(
            BurialPlot.status == "available",
            BurialPlot.deleted_at.is_(None)
        )
    )
    available_plots = result.scalar() or 0
    
    # Occupied plots
    result = await db.execute(
        select(func.count(BurialPlot.id)).where(
            BurialPlot.status == "occupied",
            BurialPlot.deleted_at.is_(None)
        )
    )
    occupied_plots = result.scalar() or 0
    
    # Reserved plots
    result = await db.execute(
        select(func.count(BurialPlot.id)).where(
            BurialPlot.status == "reserved",
            BurialPlot.deleted_at.is_(None)
        )
    )
    reserved_plots = result.scalar() or 0
    
    return {
        "total_cemeteries": total_cemeteries,
        "total_plots": total_plots,
        "available_plots": available_plots,
        "occupied_plots": occupied_plots,
        "reserved_plots": reserved_plots,
        "occupation_rate": round((occupied_plots / total_plots * 100) if total_plots > 0 else 0, 2)
    }

@router.get("/plots-by-cemetery", response_model=Dict[str, Any])
async def get_plots_by_cemetery(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get burial plots distribution by cemetery"""
    await check_permission("reports", "read", current_user, db)
    
    result = await db.execute(
        select(
            Cemetery.name,
            func.count(BurialPlot.id).label("total_plots"),
            func.sum(func.cast(BurialPlot.status == "occupied", func.Integer)).label("occupied")
        )
        .join(BurialPlot, Cemetery.id == BurialPlot.cemetery_id)
        .where(Cemetery.deleted_at.is_(None), BurialPlot.deleted_at.is_(None))
        .group_by(Cemetery.id, Cemetery.name)
    )
    
    data = []
    for row in result.all():
        data.append({
            "cemetery": row.name,
            "total_plots": row.total_plots,
            "occupied": row.occupied or 0
        })
    
    return {"data": data}
