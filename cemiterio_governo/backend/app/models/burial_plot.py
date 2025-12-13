from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class BurialPlot(Base):
    __tablename__ = "burial_plots"
    
    id = Column(Integer, primary_key=True, index=True)
    cemetery_id = Column(Integer, ForeignKey("cemeteries.id"), nullable=False)
    plot_number = Column(String, nullable=False, index=True)
    block = Column(String, nullable=True)
    row = Column(String, nullable=True)
    area_m2 = Column(Float, nullable=True)
    plot_type = Column(String, nullable=False)  # individual, familiar, etc.
    status = Column(String, nullable=False, default="available")  # available, occupied, reserved
    owner_name = Column(String, nullable=True)
    owner_document = Column(String, nullable=True)
    burial_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    # Relationships
    cemetery = relationship("Cemetery", back_populates="burial_plots")
