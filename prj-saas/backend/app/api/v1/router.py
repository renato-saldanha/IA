"""API v1 router"""

from fastapi import APIRouter
from app.api.v1 import auth, tickets, knowledge

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(tickets.router)
api_router.include_router(knowledge.router)

