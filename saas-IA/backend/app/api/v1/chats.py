from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.models import User, ChatSession, Message, ChatStatus
from app.schemas.schemas import (
    ChatSessionCreate,
    ChatSessionUpdate,
    ChatSessionResponse,
    MessageCreate,
    MessageResponse
)

router = APIRouter()


@router.post("/", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Iniciar nova sessão de chat."""
    # Verificar se já existe sessão ativa
    existing_session = db.query(ChatSession)\
        .filter(ChatSession.customer_id == current_user.id)\
        .filter(ChatSession.status == ChatStatus.ACTIVE.value)\
        .first()
    
    if existing_session:
        return existing_session
    
    # Criar nova sessão
    chat_session = ChatSession(
        customer_id=current_user.id,
        status=ChatStatus.WAITING.value
    )
    
    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)
    
    return chat_session


@router.get("/", response_model=List[ChatSessionResponse])
async def list_chat_sessions(
    status_filter: Optional[str] = Query(None, description="Filtrar por status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar sessões de chat."""
    query = db.query(ChatSession)
    
    # Clientes só veem suas próprias sessões
    if current_user.role == "customer":
        query = query.filter(ChatSession.customer_id == current_user.id)
    
    # Filtro de status
    if status_filter:
        query = query.filter(ChatSession.status == status_filter)
    
    sessions = query.order_by(ChatSession.started_at.desc()).offset(skip).limit(limit).all()
    return sessions


@router.get("/waiting", response_model=List[ChatSessionResponse])
async def get_waiting_chats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obter chats aguardando atendimento (para agentes)."""
    if current_user.role not in ["agent", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para visualizar fila de atendimento"
        )
    
    sessions = db.query(ChatSession)\
        .filter(ChatSession.status == ChatStatus.WAITING.value)\
        .order_by(ChatSession.started_at.asc())\
        .all()
    
    return sessions


@router.get("/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obter detalhes de uma sessão de chat."""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )
    
    # Verificar permissão
    if current_user.role == "customer" and session.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar esta sessão"
        )
    
    return session


@router.patch("/{session_id}", response_model=ChatSessionResponse)
async def update_chat_session(
    session_id: int,
    session_data: ChatSessionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Atualizar sessão de chat."""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )
    
    # Verificar permissão
    if current_user.role == "customer" and session.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para atualizar esta sessão"
        )
    
    # Atualizar campos
    update_data = session_data.model_dump(exclude_unset=True)
    
    # Registrar timestamp de finalização
    if "status" in update_data and update_data["status"] == ChatStatus.ENDED.value:
        update_data["ended_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(session, field, value)
    
    db.commit()
    db.refresh(session)
    
    return session


@router.post("/{session_id}/accept", response_model=ChatSessionResponse)
async def accept_chat(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Agente aceitar atendimento de chat."""
    if current_user.role not in ["agent", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para aceitar chats"
        )
    
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )
    
    if session.status != ChatStatus.WAITING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat não está aguardando atendimento"
        )
    
    session.agent_id = current_user.id
    session.status = ChatStatus.ACTIVE.value
    
    db.commit()
    db.refresh(session)
    
    return session


@router.post("/{session_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_message(
    session_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Enviar mensagem no chat."""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )
    
    # Verificar permissão
    if current_user.role == "customer" and session.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para enviar mensagem nesta sessão"
        )
    
    if current_user.role in ["agent", "admin"] and session.agent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para enviar mensagem nesta sessão"
        )
    
    message = Message(
        content=message_data.content,
        chat_session_id=session_id,
        sender_id=current_user.id
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message


@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_chat_messages(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obter mensagens de um chat."""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )
    
    # Verificar permissão
    if current_user.role == "customer" and session.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar mensagens desta sessão"
        )
    
    messages = db.query(Message)\
        .filter(Message.chat_session_id == session_id)\
        .order_by(Message.created_at.asc())\
        .all()
    
    return messages

