from fastapi import APIRouter
from app.api.v1 import auth, users, cemeteries, burial_plots, sectors, permissions, logs, reports

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(cemeteries.router, prefix="/cemeteries", tags=["cemeteries"])
api_router.include_router(burial_plots.router, prefix="/burial-plots", tags=["burial-plots"])
api_router.include_router(sectors.router, prefix="/sectors", tags=["sectors"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
