from tkhelper.database.postgres import PostgresDatabasePool
from tkhelper.database.redis import RedisConnection
from app.config import CONFIG
import os
import logging

logger = logging.Logger(__name__)

__all__ = ["postgres_pool", "redis_conn", "init_database", "close_database"]

pg_migration_script_dir = os.path.join(os.path.dirname(__file__), "pg_scripts/")
postgres_pool = PostgresDatabasePool(
    url=CONFIG.POSTGRES_URL,
    max_connections=CONFIG.POSTGRES_MAX_CONNECTIONS,
    migration_version=CONFIG.POSTGRES_SCHEMA_VERSION,
    migration_script_dir=pg_migration_script_dir,
    migration_script_filename_format=r"postgres_(\d+)(_\w+)*\.sql",
    clean_db_table_order=["c1_"],
)

redis_conn = RedisConnection(url=CONFIG.REDIS_URL)


# init postgres db pool instance
async def init_database():
    logger.info("Initializing postgres database connection pool..")
    await postgres_pool.init()

    logger.info("Initializing redis connection..")
    await redis_conn.init()


# close postgres db pool instance
async def close_database():
    logger.info("Closing postgres database connection pool..")
    await postgres_pool.close()

    logger.info("Closing redis connection..")
    await redis_conn.close()
