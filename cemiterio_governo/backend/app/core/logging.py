import logging
import sys
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.log import AuditLog

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

def setup_logging():
    """Setup application logging"""
    logger.info("Logging configured")

async def log_audit(
    session: AsyncSession,
    user_id: Optional[int],
    action: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    details: Optional[dict] = None,
    ip_address: Optional[str] = None
):
    """Log an audit event to the database"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details or {},
            ip_address=ip_address,
            created_at=datetime.utcnow()
        )
        session.add(audit_log)
        await session.commit()
        logger.info(f"Audit log created: {action} on {entity_type} by user {user_id}")
    except Exception as e:
        logger.error(f"Error creating audit log: {e}")
        await session.rollback()
