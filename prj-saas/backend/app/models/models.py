"""Database models"""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    AGENT = "agent"
    CUSTOMER = "customer"


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ChannelType(str, Enum):
    EMAIL = "email"
    CHAT = "chat"
    FORM = "form"
    WIDGET = "widget"


# Models
class Organization(SQLModel, table=True):
    __tablename__ = "organizations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    users: list["User"] = Relationship(back_populates="organization")
    tickets: list["Ticket"] = Relationship(back_populates="organization")


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    role: UserRole = Field(default=UserRole.CUSTOMER)
    is_active: bool = Field(default=True)
    organization_id: Optional[int] = Field(default=None, foreign_key="organizations.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    organization: Optional[Organization] = Relationship(back_populates="users")
    assigned_tickets: list["Ticket"] = Relationship(back_populates="assigned_to")
    messages: list["TicketMessage"] = Relationship(back_populates="author")


class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    subject: str = Field(index=True)
    description: str
    status: TicketStatus = Field(default=TicketStatus.OPEN, index=True)
    priority: TicketPriority = Field(default=TicketPriority.MEDIUM, index=True)
    channel: ChannelType = Field(default=ChannelType.FORM)
    
    # Foreign keys
    organization_id: int = Field(foreign_key="organizations.id")
    customer_id: int = Field(foreign_key="users.id")
    assigned_to_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    
    # Relationships
    organization: Organization = Relationship(back_populates="tickets")
    assigned_to: Optional[User] = Relationship(back_populates="assigned_tickets")
    messages: list["TicketMessage"] = Relationship(back_populates="ticket")
    tags: list["TicketTag"] = Relationship(back_populates="ticket")


class TicketMessage(SQLModel, table=True):
    __tablename__ = "ticket_messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    is_internal: bool = Field(default=False)
    ticket_id: int = Field(foreign_key="tickets.id", index=True)
    author_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # Relationships
    ticket: Ticket = Relationship(back_populates="messages")
    author: User = Relationship(back_populates="messages")


class TicketTag(SQLModel, table=True):
    __tablename__ = "ticket_tags"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    color: str = Field(default="#gray")
    ticket_id: int = Field(foreign_key="tickets.id", index=True)
    
    # Relationships
    ticket: Ticket = Relationship(back_populates="tags")


class KnowledgeArticle(SQLModel, table=True):
    __tablename__ = "knowledge_articles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    content: str
    category: str = Field(index=True)
    is_published: bool = Field(default=False, index=True)
    views_count: int = Field(default=0)
    organization_id: int = Field(foreign_key="organizations.id")
    author_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

