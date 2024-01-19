from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routes import routes
from common.error.exception_handlers import *
import os
import logging

# Retrieve the log level from the environment variables (defaulting to INFO).
log_level = os.environ.get("LOG_LEVEL", "INFO")

# Create a logger object.
logger = logging.getLogger()
logger.setLevel(log_level)

# Configure the log handler and format.
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a console handler.
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def create_app():
    from common.database.postgres.pool import postgres_db_pool
    from common.database.redis import redis_pool
    from common.services.auth.admin import create_default_admin_if_needed
    from common.services.model.model_schema import load_model_schema_data

    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        logger.info("FastAPI app startup...")
        await redis_pool.init_pool()
        await postgres_db_pool.init_pool()
        if CONFIG.WEB:
            await create_default_admin_if_needed()
        await load_model_schema_data()

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("FastAPI app shutdown...")
        await redis_pool.close_pool()
        await postgres_db_pool.close_pool()

    app.exception_handler(HTTPException)(custom_http_exception_handler)
    app.exception_handler(RequestValidationError)(custom_request_validation_error_handler)
    app.exception_handler(ValidationError)(custom_validation_error_handler)
    app.exception_handler(Exception)(custom_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(routes)
    return app


app = create_app()
