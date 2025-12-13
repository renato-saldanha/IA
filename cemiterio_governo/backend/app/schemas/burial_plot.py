from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class BurialPlotBase(BaseModel):
    cemetery_id: int
    plot_number: str
    block: Optional[str] = None
    row: Optional[str] = None
    area_m2: Optional[float] = None
    plot_type: str
    status: str = "available"
    owner_name: Optional[str] = None
    owner_document: Optional[str] = None
    burial_date: Optional[date] = None
    notes: Optional[str] = None

class BurialPlotCreate(BurialPlotBase):
    pass

class BurialPlotUpdate(BaseModel):
    cemetery_id: Optional[int] = None
    plot_number: Optional[str] = None
    block: Optional[str] = None
    row: Optional[str] = None
    area_m2: Optional[float] = None
    plot_type: Optional[str] = None
    status: Optional[str] = None
    owner_name: Optional[str] = None
    owner_document: Optional[str] = None
    burial_date: Optional[date] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class BurialPlot(BurialPlotBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
