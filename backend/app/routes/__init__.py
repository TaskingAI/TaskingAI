from fastapi import APIRouter
from config import CONFIG


routes = APIRouter()


def add_app_routes():
    # manage
    from app.routes.manage.manage import router as manage_router

    routes.include_router(manage_router, prefix=CONFIG.APP_ROUTE_PREFIX)

    # auth
    from app.routes.auth.apikey import router as apikey_router
    from app.routes.auth.admin import router as admin_router

    routes.include_router(apikey_router, prefix=CONFIG.APP_ROUTE_PREFIX)
    routes.include_router(admin_router, prefix=CONFIG.APP_ROUTE_PREFIX)

    # model
    from app.routes.model.model_schema import router as model_schema_router
    from app.routes.model.model import router as model_router

    routes.include_router(model_schema_router, prefix=CONFIG.APP_ROUTE_PREFIX)
    routes.include_router(model_router, prefix=CONFIG.APP_ROUTE_PREFIX)


add_app_routes()
