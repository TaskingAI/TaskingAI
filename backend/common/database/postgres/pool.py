import asyncpg
from urllib.parse import urlparse
from config import CONFIG
from typing import List
import logging

logger = logging.Logger(__name__)


def get_db_metadata_config(db_url: str):
    parsed_metadata = urlparse(db_url)
    return {
        "user": parsed_metadata.username,
        "password": parsed_metadata.password,
        "database": parsed_metadata.path.lstrip("/"),
        "host": parsed_metadata.hostname,
        "port": parsed_metadata.port,
    }


class PostgresDatabasePool:
    def __init__(
        self,
        url: str,
        max_connections: int,
        migration_version: int,
        migration_script_dir: str,
        migration_script_filename_format: str,
        clean_db_table_order: List,
    ):
        """
        Initialize postgres database connection pool
        :param url: database url
        :param max_connections: max connections in pool
        """

        self.url = url
        self.max_connections = max_connections
        self.db_pool = None
        self.db_name = None
        self.migration_version = migration_version
        self.migration_script_dir = migration_script_dir
        self.migration_script_filename_format = migration_script_filename_format
        self.clean_db_table_order = clean_db_table_order

    async def init_pool(self):
        """Initialize database connection pool"""

        db_config = get_db_metadata_config(self.url)
        self.db_name = db_config["database"]
        self.db_pool = await asyncpg.create_pool(
            **db_config,
            min_size=min(self.max_connections // 2 + 1, self.max_connections),
            max_size=self.max_connections,
        )
        await self._migration_if_needed()

    async def clean_data(self):
        """Clean all data in database and reinitialize it"""
        from .manage import clean_data

        if not CONFIG.TEST and not CONFIG.DEV:
            raise Exception("Cannot clean data in production environment")

        async with self.db_pool.acquire() as conn:
            await clean_data(conn, table_name_order=self.clean_db_table_order)
            logger.info(f"Postgres database {self.db_name} clean done.")

        await self._migration_if_needed()

    async def _migration_if_needed(self):
        """Migrate database if needed"""

        from .migrate import migrate_if_needed

        async with self.db_pool.acquire() as conn:
            await migrate_if_needed(
                conn,
                latest_version=self.migration_version,
                db_name=self.db_name,
                migration_script_dir=self.migration_script_dir,
                migration_script_filename_format=self.migration_script_filename_format,
            )
            logger.info(f"Postgres database {self.db_name} migration done.")

    async def close_pool(self):
        """Close database connection pool"""

        if self.db_pool is not None:
            await self.db_pool.close()
            logger.info(f"Postgres database {self.db_name} pool closed.")

    async def get_db_connection(self):
        """Get database connection from pool"""

        async with self.db_pool.acquire() as connection:
            try:
                yield connection
            finally:
                await self.db_pool.release(connection)


# init postgres db pool instance
postgres_db_pool = PostgresDatabasePool(
    url=CONFIG.POSTGRES_URL,
    max_connections=CONFIG.POSTGRES_MAX_CONNECTIONS,
    migration_version=CONFIG.POSTGRES_SCHEMA_VERSION,
    migration_script_dir="scripts/postgres/",
    migration_script_filename_format=r"postgres_(\d+).sql",
    clean_db_table_order=[],
)
