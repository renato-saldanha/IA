from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    sector_id = Column(Integer, ForeignKey("sectors.id"), nullable=False)
    resource = Column(String, nullable=False)  # cemeteries, burial_plots, reports, etc.
    action = Column(String, nullable=False)  # create, read, update, delete
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    # Relationships
    sector = relationship("Sector", back_populates="permissions")
    user_permissions = relationship("UserPermission", back_populates="permission", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('sector_id', 'resource', 'action', name='uq_sector_resource_action'),
    )

class UserPermission(Base):
    __tablename__ = "user_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="permissions")
    permission = relationship("Permission", back_populates="user_permissions")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'permission_id', name='uq_user_permission'),
    )
