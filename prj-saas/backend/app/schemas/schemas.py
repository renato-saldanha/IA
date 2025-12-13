"""Pydantic schemas for request/response"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.models import UserRole, TicketStatus, TicketPriority, ChannelType


# Auth schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    organization_name: Optional[str] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None
    type: Optional[str] = None


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.CUSTOMER


class UserCreate(UserBase):
    password: str
    organization_id: Optional[int] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    organization_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Organization schemas
class OrganizationBase(BaseModel):
    name: str
    slug: str


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Ticket schemas
class TicketBase(BaseModel):
    subject: str
    description: str
    priority: TicketPriority = TicketPriority.MEDIUM
    channel: ChannelType = ChannelType.FORM


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigned_to_id: Optional[int] = None


class TicketResponse(TicketBase):
    id: int
    status: TicketStatus
    organization_id: int
    customer_id: int
    assigned_to_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    closed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Message schemas
class TicketMessageBase(BaseModel):
    content: str
    is_internal: bool = False


class TicketMessageCreate(TicketMessageBase):
    ticket_id: int


class TicketMessageResponse(TicketMessageBase):
    id: int
    ticket_id: int
    author_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Knowledge Article schemas
class KnowledgeArticleBase(BaseModel):
    title: str
    slug: str
    content: str
    category: str
    is_published: bool = False


class KnowledgeArticleCreate(KnowledgeArticleBase):
    pass


class KnowledgeArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    is_published: Optional[bool] = None


class KnowledgeArticleResponse(KnowledgeArticleBase):
    id: int
    views_count: int
    organization_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

