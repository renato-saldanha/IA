"""Knowledge base routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional

from app.db.session import get_session
from app.api.deps import get_current_user, get_current_agent_or_admin
from app.schemas.schemas import KnowledgeArticleCreate, KnowledgeArticleUpdate, KnowledgeArticleResponse
from app.models.models import KnowledgeArticle, User

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.post("", response_model=KnowledgeArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: KnowledgeArticleCreate,
    current_user: User = Depends(get_current_agent_or_admin),
    session: Session = Depends(get_session)
):
    """Create knowledge article (agents/admins only)"""
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )
    
    article = KnowledgeArticle(
        **article_data.model_dump(),
        organization_id=current_user.organization_id,
        author_id=current_user.id
    )
    session.add(article)
    session.commit()
    session.refresh(article)
    
    return article


@router.get("", response_model=List[KnowledgeArticleResponse])
async def list_articles(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    published_only: bool = True,
    skip: int = 0,
    limit: int = 50,
    current_user: Optional[User] = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List knowledge articles"""
    query = select(KnowledgeArticle).where(
        KnowledgeArticle.organization_id == current_user.organization_id
    )
    
    if published_only:
        query = query.where(KnowledgeArticle.is_published == True)
    
    if category:
        query = query.where(KnowledgeArticle.category == category)
    
    if search:
        query = query.where(
            KnowledgeArticle.title.contains(search) | 
            KnowledgeArticle.content.contains(search)
        )
    
    query = query.offset(skip).limit(limit).order_by(KnowledgeArticle.created_at.desc())
    articles = session.exec(query).all()
    
    return articles


@router.get("/{article_id}", response_model=KnowledgeArticleResponse)
async def get_article(
    article_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get article by ID"""
    article = session.get(KnowledgeArticle, article_id)
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    if article.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Increment view count
    article.views_count += 1
    session.add(article)
    session.commit()
    session.refresh(article)
    
    return article


@router.patch("/{article_id}", response_model=KnowledgeArticleResponse)
async def update_article(
    article_id: int,
    article_data: KnowledgeArticleUpdate,
    current_user: User = Depends(get_current_agent_or_admin),
    session: Session = Depends(get_session)
):
    """Update article (agents/admins only)"""
    article = session.get(KnowledgeArticle, article_id)
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    if article.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    for key, value in article_data.model_dump(exclude_unset=True).items():
        setattr(article, key, value)
    
    from datetime import datetime
    article.updated_at = datetime.utcnow()
    
    session.add(article)
    session.commit()
    session.refresh(article)
    
    return article


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_agent_or_admin),
    session: Session = Depends(get_session)
):
    """Delete article (agents/admins only)"""
    article = session.get(KnowledgeArticle, article_id)
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    if article.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    session.delete(article)
    session.commit()

