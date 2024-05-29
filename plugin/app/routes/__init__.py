from fastapi import APIRouter
from config import CONFIG

from app.routes.image import router as images_router
from app.routes.plugin import router as list_plugin_router
from app.routes.bundle import router as list_bundle_router
from app.routes.manage import router as manage_router
from app.routes.execute import router as execute_router
from app.routes.verify import router as verify_credentials_router

routes = APIRouter()
routes.include_router(images_router, prefix=CONFIG.IMAGE_ROUTE_PREFIX)
routes.include_router(list_plugin_router, prefix=CONFIG.API_ROUTE_PREFIX)
routes.include_router(list_bundle_router, prefix=CONFIG.API_ROUTE_PREFIX)
routes.include_router(manage_router, prefix=CONFIG.API_ROUTE_PREFIX)
routes.include_router(execute_router, prefix=CONFIG.API_ROUTE_PREFIX)
routes.include_router(verify_credentials_router, prefix=CONFIG.API_ROUTE_PREFIX)
