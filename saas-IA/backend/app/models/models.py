from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    AGENT = "agent"
    CUSTOMER = "customer"


class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ChatStatus(str, enum.Enum):
    ACTIVE = "active"
    WAITING = "waiting"
    ENDED = "ended"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_online = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    tickets_created = relationship("Ticket", back_populates="customer", foreign_keys="Ticket.customer_id")
    tickets_assigned = relationship("Ticket", back_populates="assigned_agent", foreign_keys="Ticket.assigned_to")
    messages = relationship("Message", back_populates="sender")
    chat_sessions = relationship("ChatSession", back_populates="customer")
    articles_created = relationship("KnowledgeArticle", back_populates="author")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False, index=True)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False)
    category = Column(String, nullable=True, index=True)
    
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)

    # Relacionamentos
    customer = relationship("User", back_populates="tickets_created", foreign_keys=[customer_id])
    assigned_agent = relationship("User", back_populates="tickets_assigned", foreign_keys=[assigned_to])
    messages = relationship("Message", back_populates="ticket", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)  # Notas internas entre agentes
    
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    chat_session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    read_at = Column(DateTime, nullable=True)

    # Relacionamentos
    ticket = relationship("Ticket", back_populates="messages")
    chat_session = relationship("ChatSession", back_populates="messages")
    sender = relationship("User", back_populates="messages")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(ChatStatus), default=ChatStatus.WAITING, nullable=False, index=True)
    
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 estrelas
    feedback = Column(Text, nullable=True)

    # Relacionamentos
    customer = relationship("User", back_populates="chat_sessions", foreign_keys=[customer_id])
    messages = relationship("Message", back_populates="chat_session", cascade="all, delete-orphan")


class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=True, index=True)
    tags = Column(String, nullable=True)  # Comma-separated tags
    
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    is_published = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)

    # Relacionamentos
    author = relationship("User", back_populates="articles_created")

