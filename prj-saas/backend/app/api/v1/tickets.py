"""Tickets routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional

from app.db.session import get_session
from app.api.deps import get_current_user, get_current_agent_or_admin
from app.schemas.schemas import TicketCreate, TicketUpdate, TicketResponse, TicketMessageCreate, TicketMessageResponse
from app.models.models import Ticket, User, TicketMessage, UserRole, TicketStatus

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new ticket"""
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )
    
    ticket = Ticket(
        **ticket_data.model_dump(),
        organization_id=current_user.organization_id,
        customer_id=current_user.id
    )
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    
    return ticket


@router.get("", response_model=List[TicketResponse])
async def list_tickets(
    status_filter: Optional[TicketStatus] = Query(None),
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List tickets"""
    query = select(Ticket).where(Ticket.organization_id == current_user.organization_id)
    
    # Customers only see their own tickets
    if current_user.role == UserRole.CUSTOMER:
        query = query.where(Ticket.customer_id == current_user.id)
    
    if status_filter:
        query = query.where(Ticket.status == status_filter)
    
    query = query.offset(skip).limit(limit).order_by(Ticket.created_at.desc())
    tickets = session.exec(query).all()
    
    return tickets


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get ticket by ID"""
    ticket = session.get(Ticket, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # Check permissions
    if ticket.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if current_user.role == UserRole.CUSTOMER and ticket.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    current_user: User = Depends(get_current_agent_or_admin),
    session: Session = Depends(get_session)
):
    """Update ticket (agents/admins only)"""
    ticket = session.get(Ticket, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    if ticket.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    for key, value in ticket_data.model_dump(exclude_unset=True).items():
        setattr(ticket, key, value)
    
    from datetime import datetime
    ticket.updated_at = datetime.utcnow()
    
    if ticket_data.status == TicketStatus.RESOLVED and not ticket.resolved_at:
        ticket.resolved_at = datetime.utcnow()
    elif ticket_data.status == TicketStatus.CLOSED and not ticket.closed_at:
        ticket.closed_at = datetime.utcnow()
    
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    
    return ticket


@router.post("/{ticket_id}/messages", response_model=TicketMessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    ticket_id: int,
    message_data: TicketMessageCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Add message to ticket"""
    ticket = session.get(Ticket, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    if ticket.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Only agents/admins can create internal messages
    if message_data.is_internal and current_user.role == UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    message = TicketMessage(
        content=message_data.content,
        is_internal=message_data.is_internal,
        ticket_id=ticket_id,
        author_id=current_user.id
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    
    return message


@router.get("/{ticket_id}/messages", response_model=List[TicketMessageResponse])
async def list_messages(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List ticket messages"""
    ticket = session.get(Ticket, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    if ticket.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    query = select(TicketMessage).where(TicketMessage.ticket_id == ticket_id)
    
    # Customers don't see internal messages
    if current_user.role == UserRole.CUSTOMER:
        query = query.where(TicketMessage.is_internal == False)
    
    query = query.order_by(TicketMessage.created_at)
    messages = session.exec(query).all()
    
    return messages

