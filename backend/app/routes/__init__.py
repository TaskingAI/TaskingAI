from fastapi import APIRouter
from config import CONFIG


routes = APIRouter()


def add_app_routes():
    from app.routes.manage.manage import router as manage_router
    from app.routes.auth.apikey import router as apikey_router
    from app.routes.auth.admin import router as admin_router

    routes.include_router(manage_router, prefix=CONFIG.APP_ROUTE_PREFIX)
    routes.include_router(apikey_router, prefix=CONFIG.APP_ROUTE_PREFIX)
    routes.include_router(admin_router, prefix=CONFIG.APP_ROUTE_PREFIX)


add_app_routes()
