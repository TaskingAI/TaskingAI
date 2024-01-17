from fastapi import APIRouter
from config import CONFIG

routes = APIRouter()


def add_manage_routes(route_prefix: str):
    from app.routes.manage.manage import router as manage_router

    routes.include_router(manage_router, prefix=route_prefix)


def add_auth_routes(route_prefix: str):
    from app.routes.auth.apikey import router as apikey_router
    from app.routes.auth.admin import router as admin_router

    routes.include_router(apikey_router, prefix=route_prefix)
    routes.include_router(admin_router, prefix=route_prefix)


def add_model_routes(route_prefix: str):
    from app.routes.model.model_schema import router as model_schema_router
    from app.routes.model.model import router as model_router

    routes.include_router(model_schema_router, prefix=route_prefix)
    routes.include_router(model_router, prefix=route_prefix)


def add_tool_routes(route_prefix: str):
    from app.routes.tool.action import router as action_router

    routes.include_router(action_router, prefix=route_prefix)


def add_retrieval_routes(route_prefix: str):
    from app.routes.retrieval.collection import router as collection_router
    from app.routes.retrieval.record import router as record_router
    from app.routes.retrieval.chunk import router as chunk_router

    routes.include_router(collection_router, prefix=route_prefix)
    routes.include_router(record_router, prefix=route_prefix)
    routes.include_router(chunk_router, prefix=route_prefix)


def add_inference_routes(route_prefix: str):
    from app.routes.inference.text_embedding import router as text_embedding_router
    from app.routes.inference.chat_completion import router as chat_completion_router

    routes.include_router(text_embedding_router, prefix=route_prefix)
    routes.include_router(chat_completion_router, prefix=route_prefix)


def add_assistant_routes(route_prefix: str):
    from app.routes.assistant.assistant import router as assistant_router
    from app.routes.assistant.chat import router as chat_router
    from app.routes.assistant.message import router as message_router
    from app.routes.assistant.generation import router as generation_router

    routes.include_router(assistant_router, prefix=route_prefix)
    routes.include_router(chat_router, prefix=route_prefix)
    routes.include_router(message_router, prefix=route_prefix)
    routes.include_router(generation_router, prefix=route_prefix)


if CONFIG.WEB:
    add_manage_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_auth_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_model_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_tool_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_retrieval_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_inference_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_assistant_routes(CONFIG.WEB_ROUTE_PREFIX)


elif CONFIG.API:
    add_manage_routes(CONFIG.API_ROUTE_PREFIX)
    add_tool_routes(CONFIG.API_ROUTE_PREFIX)
    add_retrieval_routes(CONFIG.API_ROUTE_PREFIX)
    add_inference_routes(CONFIG.API_ROUTE_PREFIX)
    add_assistant_routes(CONFIG.API_ROUTE_PREFIX)
