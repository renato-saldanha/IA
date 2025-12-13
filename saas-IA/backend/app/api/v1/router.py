from fastapi import APIRouter
from . import auth, tickets, knowledge, chats

api_router = APIRouter()

# Incluir routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge Base"])
api_router.include_router(chats.router, prefix="/chats", tags=["Live Chat"])

