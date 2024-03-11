import logging
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from starlette.middleware.cors import CORSMiddleware
from tkhelper.error.exception_handlers import *
from tkhelper.utils import init_logger

from contextlib import asynccontextmanager

init_logger()
logger = logging.getLogger(__name__)
_scheduler = AsyncIOScheduler()


async def sync_data(first_sync=False):
    from app.services.model import sync_model_schema_data
    from app.services.tool import sync_plugin_data

    try:
        logger.info("Syncing model schema data...")
        await sync_model_schema_data()
        logger.info("Syncing plugin data...")
        await sync_plugin_data()
    except:
        logger.error("Failed to sync model schema data.")
        if first_sync:
            raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import close_database, init_database
    from app.services.auth.admin import create_default_admin_if_needed
    from app.config import CONFIG

    try:
        logger.info("fastapi app startup...")

        logger.info("start plugin cache scheduler...")
        _scheduler.add_job(sync_data, "interval", minutes=1)
        _scheduler.start()
        # first sync
        await sync_data(first_sync=True)

        await init_database()
        if CONFIG.WEB:
            await create_default_admin_if_needed()

        yield

    finally:
        logger.info("fastapi app shutdown...")
        await close_database()


def create_app():
    from app.config import CONFIG
    from app.routes import routes

    app = FastAPI(title="TaskingAI-Community", version=CONFIG.VERSION, lifespan=lifespan)

    # add exception handlers
    add_exception_handlers(app)

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
