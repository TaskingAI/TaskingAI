from typing import List

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from starlette_prometheus import metrics, PrometheusMiddleware
from app.routes import routes
import logging
import os
from app.error.exception_handlers import *
from app.cache import (
    load_bundle_data,
    load_all_bundle_handlers,
    load_plugin_data,
    load_all_plugin_handlers,
    set_i18n_checksum,
)

import warnings

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

    try:
        logger.info("fastapi app startup...")
        logger.info("load all bundles and plugins")
        bundle_ids = load_bundle_data()
        load_all_bundle_handlers(bundle_ids)
        bundle_plugin_ids = load_plugin_data(bundle_ids)
        load_all_plugin_handlers(bundle_plugin_ids)
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
        title="TaskingAI-Plugin",
        version=CONFIG.VERSION,
        servers=[{f"url": f"http://localhost:{CONFIG.SERVICE_PORT}"}],
        lifespan=lifespan,
    )

    init_route_logger(filters=["/health_check", "/prometheus/metrics", "/cache_checksums"])

    app.exception_handler(HTTPException)(custom_http_exception_handler)
    app.exception_handler(RequestValidationError)(custom_request_validation_error_handler)
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
