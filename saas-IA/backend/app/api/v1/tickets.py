from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.models import User, Ticket, Message, TicketStatus
from app.schemas.schemas import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    MessageCreate,
    MessageResponse
)

router = APIRouter()


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Criar novo ticket de suporte."""
    ticket = Ticket(
        **ticket_data.model_dump(),
        customer_id=current_user.id
    )
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    return ticket


@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    status_filter: Optional[str] = Query(None, description="Filtrar por status"),
    priority: Optional[str] = Query(None, description="Filtrar por prioridade"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar tickets do usuário ou todos (se agente/admin)."""
    query = db.query(Ticket)
    
    # Clientes só veem seus próprios tickets
    if current_user.role == "customer":
        query = query.filter(Ticket.customer_id == current_user.id)
    
    # Filtros
    if status_filter:
        query = query.filter(Ticket.status == status_filter)
    if priority:
        query = query.filter(Ticket.priority == priority)
    
    tickets = query.order_by(Ticket.created_at.desc()).offset(skip).limit(limit).all()
    return tickets


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obter detalhes de um ticket."""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket não encontrado"
        )
    
    # Verificar permissão
    if current_user.role == "customer" and ticket.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar este ticket"
        )
    
    return ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Atualizar ticket."""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket não encontrado"
        )
    
    # Verificar permissão
    if current_user.role == "customer" and ticket.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para atualizar este ticket"
        )
    
    # Atualizar campos
    update_data = ticket_data.model_dump(exclude_unset=True)
    
    # Registrar timestamps
    if "status" in update_data:
        if update_data["status"] == TicketStatus.RESOLVED.value:
            update_data["resolved_at"] = datetime.utcnow()
        elif update_data["status"] == TicketStatus.CLOSED.value:
            update_data["closed_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(ticket, field, value)
    
    db.commit()
    db.refresh(ticket)
    
    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Deletar ticket (apenas admin)."""
    if current_user.role not in ["admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para deletar tickets"
        )
    
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket não encontrado"
        )
    
    db.delete(ticket)
    db.commit()
    
    return None


@router.post("/{ticket_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    ticket_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Adicionar mensagem a um ticket."""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket não encontrado"
        )
    
    # Verificar permissão
    if current_user.role == "customer" and ticket.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para adicionar mensagem neste ticket"
        )
    
    message = Message(
        content=message_data.content,
        is_internal=message_data.is_internal,
        ticket_id=ticket_id,
        sender_id=current_user.id
    )
    
    db.add(message)
    
    # Atualizar status do ticket se estava resolvido
    if ticket.status == TicketStatus.RESOLVED.value:
        ticket.status = TicketStatus.OPEN.value
    
    db.commit()
    db.refresh(message)
    
    return message


@router.get("/{ticket_id}/messages", response_model=List[MessageResponse])
async def get_ticket_messages(
    ticket_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obter mensagens de um ticket."""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket não encontrado"
        )
    
    # Verificar permissão
    if current_user.role == "customer" and ticket.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar mensagens deste ticket"
        )
    
    query = db.query(Message).filter(Message.ticket_id == ticket_id)
    
    # Clientes não veem mensagens internas
    if current_user.role == "customer":
        query = query.filter(Message.is_internal == False)
    
    messages = query.order_by(Message.created_at.asc()).all()
    return messages

