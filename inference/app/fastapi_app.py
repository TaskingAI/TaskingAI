from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import routes
from app.error.exception_handlers import *
import logging
import os
import warnings
from starlette_prometheus import metrics, PrometheusMiddleware


warnings.filterwarnings("ignore", module="pydantic")

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


@asynccontextmanager
async def lifespan(app: FastAPI):

    from app.cache import (
        load_model_schema_data,
        load_provider_data,
        load_all_text_embedding_models,
        load_all_chat_completion_models,
    )
    from app.utils import set_i18n_checksum

    try:
        logger.info("fastapi app startup...")
        provider_ids = load_provider_data()
        load_model_schema_data(provider_ids)
        load_all_text_embedding_models(provider_ids)
        load_all_chat_completion_models(provider_ids)
        set_i18n_checksum()
        yield

    finally:
        logger.info("fastapi app shutdown...")


def init_route_logger(filters: List[str]):

    logger = logging.getLogger("uvicorn.access")
    if logger.handlers:
        handler = logger.handlers[0]
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    else:
        # create a logging format
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        # create a stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        # add the stream handler to the logger
        logger.addHandler(stream_handler)

    class IgnoreRouteLogFilter(logging.Filter):
        def filter(self, record):
            message = record.getMessage()
            return not any([f in message for f in filters])

    logger.addFilter(IgnoreRouteLogFilter())


def create_app():

    app = FastAPI(
        title="TaskingAI-Inference",
        version=CONFIG.VERSION,
        servers=[{f"url": f"http://localhost:{CONFIG.SERVICE_PORT}"}],
        lifespan=lifespan,
    )

    init_route_logger(filters=[' HTTP/1.1" 200'])
    app.exception_handler(HTTPException)(custom_http_exception_handler)
    app.exception_handler(RequestValidationError)(custom_request_validation_error_handler)
    # app.exception_handler(ValidationError)(custom_validation_error_handler)
    app.exception_handler(Exception)(custom_exception_handler)

    app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True)
    app.add_route("/prometheus/metrics", metrics)

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
