from fastapi import APIRouter
from config import CONFIG


routes = APIRouter()


def add_routes(route_prefix: str):
    # manage
    from app.routes.manage.manage import router as manage_router

    routes.include_router(manage_router, prefix=route_prefix)

    # auth
    from app.routes.auth.apikey import router as apikey_router
    from app.routes.auth.admin import router as admin_router

    routes.include_router(apikey_router, prefix=route_prefix)
    routes.include_router(admin_router, prefix=route_prefix)

    # model
    from app.routes.model.model_schema import router as model_schema_router
    from app.routes.model.model import router as model_router

    routes.include_router(model_schema_router, prefix=route_prefix)
    routes.include_router(model_router, prefix=route_prefix)

    # tool
    from app.routes.tool.action import router as action_router

    routes.include_router(action_router, prefix=route_prefix)

    # retrieval
    from app.routes.retrieval.collection import router as collection_router
    from app.routes.retrieval.record import router as record_router
    from app.routes.retrieval.chunk import router as chunk_router

    routes.include_router(collection_router, prefix=route_prefix)
    routes.include_router(record_router, prefix=route_prefix)
    routes.include_router(chunk_router, prefix=route_prefix)


add_routes(CONFIG.APP_ROUTE_PREFIX)
