from fastapi import APIRouter
from config import CONFIG

from app.routes.manage.manage import router as manage_router


routes = APIRouter()
routes.include_router(manage_router, prefix=CONFIG.API_ROUTE_PREFIX)
