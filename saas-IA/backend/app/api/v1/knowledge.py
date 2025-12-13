from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.models import User, KnowledgeArticle
from app.schemas.schemas import (
    KnowledgeArticleCreate,
    KnowledgeArticleUpdate,
    KnowledgeArticleResponse
)

router = APIRouter()


@router.post("/", response_model=KnowledgeArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: KnowledgeArticleCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Criar artigo da base de conhecimento (agente/admin)."""
    if current_user.role not in ["agent", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para criar artigos"
        )
    
    article = KnowledgeArticle(
        **article_data.model_dump(),
        author_id=current_user.id
    )
    
    db.add(article)
    db.commit()
    db.refresh(article)
    
    return article


@router.get("/", response_model=List[KnowledgeArticleResponse])
async def list_articles(
    search: Optional[str] = Query(None, description="Buscar em título e conteúdo"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    published_only: bool = Query(True, description="Apenas artigos publicados"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Listar artigos da base de conhecimento."""
    query = db.query(KnowledgeArticle)
    
    # Filtro de publicação
    if published_only:
        query = query.filter(KnowledgeArticle.is_published == True)
    
    # Filtro de categoria
    if category:
        query = query.filter(KnowledgeArticle.category == category)
    
    # Busca textual
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                KnowledgeArticle.title.ilike(search_term),
                KnowledgeArticle.content.ilike(search_term),
                KnowledgeArticle.tags.ilike(search_term)
            )
        )
    
    articles = query.order_by(KnowledgeArticle.view_count.desc()).offset(skip).limit(limit).all()
    return articles


@router.get("/{article_id}", response_model=KnowledgeArticleResponse)
async def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """Obter artigo por ID."""
    article = db.query(KnowledgeArticle).filter(KnowledgeArticle.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artigo não encontrado"
        )
    
    if not article.is_published:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artigo não disponível"
        )
    
    # Incrementar contador de visualizações
    article.view_count += 1
    db.commit()
    
    return article


@router.patch("/{article_id}", response_model=KnowledgeArticleResponse)
async def update_article(
    article_id: int,
    article_data: KnowledgeArticleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Atualizar artigo (agente/admin)."""
    if current_user.role not in ["agent", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para atualizar artigos"
        )
    
    article = db.query(KnowledgeArticle).filter(KnowledgeArticle.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artigo não encontrado"
        )
    
    # Atualizar campos
    update_data = article_data.model_dump(exclude_unset=True)
    
    # Registrar data de publicação
    if "is_published" in update_data and update_data["is_published"] and not article.published_at:
        update_data["published_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(article, field, value)
    
    db.commit()
    db.refresh(article)
    
    return article


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Deletar artigo (admin)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para deletar artigos"
        )
    
    article = db.query(KnowledgeArticle).filter(KnowledgeArticle.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artigo não encontrado"
        )
    
    db.delete(article)
    db.commit()
    
    return None


@router.post("/{article_id}/helpful", response_model=KnowledgeArticleResponse)
async def mark_helpful(
    article_id: int,
    db: Session = Depends(get_db)
):
    """Marcar artigo como útil."""
    article = db.query(KnowledgeArticle).filter(KnowledgeArticle.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artigo não encontrado"
        )
    
    article.helpful_count += 1
    db.commit()
    db.refresh(article)
    
    return article


@router.get("/categories/list", response_model=List[str])
async def list_categories(db: Session = Depends(get_db)):
    """Listar todas as categorias disponíveis."""
    categories = db.query(KnowledgeArticle.category)\
        .filter(KnowledgeArticle.category.isnot(None))\
        .filter(KnowledgeArticle.is_published == True)\
        .distinct()\
        .all()
    
    return [cat[0] for cat in categories if cat[0]]

