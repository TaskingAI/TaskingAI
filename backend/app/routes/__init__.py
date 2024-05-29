from fastapi import APIRouter
from app.config import CONFIG


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

    routes.include_router(model_schema_router, prefix=route_prefix)


def add_tool_action_routes(route_prefix: str):
    from app.routes.tool.action import router as action_router

    routes.include_router(action_router, prefix=route_prefix)


def add_tool_plugin_routes(route_prefix: str):
    from app.routes.tool.plugin import router as action_router

    routes.include_router(action_router, prefix=route_prefix)


def add_retrieval_routes(route_prefix: str):
    from app.routes.retrieval.chunk import router as chunk_router

    routes.include_router(chunk_router, prefix=route_prefix)


def add_inference_routes(route_prefix: str):
    from app.routes.inference.text_embedding import router as text_embedding_router
    from app.routes.inference.chat_completion import router as chat_completion_router
    from app.routes.inference.rerank import router as rerank_router

    routes.include_router(text_embedding_router, prefix=route_prefix)
    routes.include_router(chat_completion_router, prefix=route_prefix)
    routes.include_router(rerank_router, prefix=route_prefix)


def add_openai_routes(route_prefix: str):
    from app.routes.openai.chat_completion import router as openai_chat_completion_router
    from app.routes.openai.text_embedding import router as openai_text_embedding_router

    routes.include_router(openai_chat_completion_router, prefix=route_prefix)
    routes.include_router(openai_text_embedding_router, prefix=route_prefix)

def add_assistant_routes(route_prefix: str):
    from app.routes.assistant.generation import router as generation_router

    routes.include_router(generation_router, prefix=route_prefix)


def add_file_routes(route_prefix: str):
    from app.routes.file.file import router as file_router
    from app.routes.file.image import router as image_router

    routes.include_router(file_router, prefix=route_prefix)
    routes.include_router(image_router, prefix=route_prefix)


def add_ui_routes(route_prefix: str):
    from app.routes.ui.sample_code import router as sample_code_router
    from app.routes.ui.assistant import router as assistant_router
    from app.routes.ui.collection import router as collection_router

    routes.include_router(sample_code_router, prefix=route_prefix)
    routes.include_router(assistant_router, prefix=route_prefix)
    routes.include_router(collection_router, prefix=route_prefix)


if CONFIG.WEB:
    add_manage_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_auth_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_model_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_tool_action_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_tool_plugin_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_retrieval_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_inference_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_assistant_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_file_routes(CONFIG.WEB_ROUTE_PREFIX)
    add_ui_routes(CONFIG.WEB_ROUTE_PREFIX)

    from app.routes.auto import *

    router = APIRouter()
    auto_add_apikey_routes(router)  # auth
    auto_add_assistant_routes(router)  # assistant
    auto_add_chat_routes(router)
    auto_add_message_routes(router)
    auto_add_collection_routes(router)  # retrieval
    auto_add_record_routes(router)
    auto_add_chunk_routes(router)
    auto_add_action_routes(router)  # tool
    auto_add_bundle_instance_routes(router)
    auto_add_model_routes(router)  # model
    routes.include_router(router, prefix=CONFIG.WEB_ROUTE_PREFIX)


elif CONFIG.API:
    add_manage_routes(CONFIG.API_ROUTE_PREFIX)
    add_tool_action_routes(CONFIG.API_ROUTE_PREFIX)
    add_retrieval_routes(CONFIG.API_ROUTE_PREFIX)
    add_inference_routes(CONFIG.API_ROUTE_PREFIX)
    add_openai_routes(CONFIG.API_ROUTE_PREFIX)
    add_assistant_routes(CONFIG.API_ROUTE_PREFIX)
    add_file_routes(CONFIG.API_ROUTE_PREFIX)

    from app.routes.auto import *

    router = APIRouter()
    auto_add_assistant_routes(router)  # assistant
    auto_add_chat_routes(router)
    auto_add_message_routes(router)
    auto_add_collection_routes(router)  # retrieval
    auto_add_record_routes(router)
    auto_add_chunk_routes(router)
    auto_add_action_routes(router)  # tool
    routes.include_router(router, prefix=CONFIG.API_ROUTE_PREFIX)
