from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ===== User Schemas =====
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "customer"


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_online: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_online: bool
    avatar_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ===== Ticket Schemas =====
class TicketBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    priority: str = "medium"
    category: Optional[str] = None


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    assigned_to: Optional[int] = None


class TicketResponse(TicketBase):
    id: int
    status: str
    customer_id: int
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== Message Schemas =====
class MessageBase(BaseModel):
    content: str = Field(..., min_length=1)
    is_internal: bool = False


class MessageCreate(MessageBase):
    ticket_id: Optional[int] = None
    chat_session_id: Optional[int] = None


class MessageResponse(MessageBase):
    id: int
    ticket_id: Optional[int] = None
    chat_session_id: Optional[int] = None
    sender_id: int
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== Chat Session Schemas =====
class ChatSessionBase(BaseModel):
    pass


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    status: Optional[str] = None
    agent_id: Optional[int] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    feedback: Optional[str] = None


class ChatSessionResponse(ChatSessionBase):
    id: int
    status: str
    customer_id: int
    agent_id: Optional[int] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    rating: Optional[int] = None
    feedback: Optional[str] = None

    class Config:
        from_attributes = True


# ===== Knowledge Article Schemas =====
class KnowledgeArticleBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=20)
    category: Optional[str] = None
    tags: Optional[str] = None


class KnowledgeArticleCreate(KnowledgeArticleBase):
    pass


class KnowledgeArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    content: Optional[str] = Field(None, min_length=20)
    category: Optional[str] = None
    tags: Optional[str] = None
    is_published: Optional[bool] = None


class KnowledgeArticleResponse(KnowledgeArticleBase):
    id: int
    author_id: int
    is_published: bool
    view_count: int
    helpful_count: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== Authentication Schemas =====
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

