from fastapi import APIRouter
from config import CONFIG

routes = APIRouter()


from app.routes.chat_completion.route import router as chat_completion_router

routes.include_router(chat_completion_router, prefix=CONFIG.API_ROUTE_PREFIX)

from app.routes.text_embedding.route import router as text_embedding_router

routes.include_router(text_embedding_router, prefix=CONFIG.API_ROUTE_PREFIX)

from app.routes.verify.route import router as verify_credentials_router

routes.include_router(verify_credentials_router, prefix=CONFIG.API_ROUTE_PREFIX)

from app.routes.model.route import router as model_router

routes.include_router(model_router, prefix=CONFIG.API_ROUTE_PREFIX)

from app.routes.manage.route import router as manage_router

routes.include_router(manage_router, prefix=CONFIG.API_ROUTE_PREFIX)

from app.routes.images.route import router as images_router

routes.include_router(images_router, prefix=CONFIG.IMAGE_ROUTE_PREFIX)

from app.routes.rerank.route import router as rerank_router

routes.include_router(rerank_router, prefix=CONFIG.API_ROUTE_PREFIX)
