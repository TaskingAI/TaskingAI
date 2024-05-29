import asyncpg
from urllib.parse import urlparse
from typing import List
import os

# from tkhelper.utils import get_logger
import logging

logger = logging.getLogger(__name__)
MODE = os.environ.get("MODE", "prod").lower()


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

    # -- connection management --

    async def init(self):
        """Initialize database connection pool"""

        db_config = get_db_metadata_config(self.url)
        self.db_name = db_config["database"]
        self.db_pool = await asyncpg.create_pool(
            **db_config,
            min_size=min(self.max_connections // 2 + 1, self.max_connections),
            max_size=self.max_connections,
        )
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

    async def close(self):
        """Close database connection pool"""

        if self.db_pool is not None:
            await self.db_pool.close()
            logger.info(f"Postgres database {self.db_name} pool closed.")

    def get_db_connection(self):
        """Get database connection from pool"""
        return self.db_pool.acquire()

    # -- clean --

    async def clean_data(self):
        """Clean all data in database and reinitialize it"""
        from .manage import clean_data

        if MODE == "prod":
            raise Exception("Cannot clean cassandra data in production mode")

        async with self.db_pool.acquire() as conn:
            await clean_data(conn, table_name_order=self.clean_db_table_order)
            logger.info(f"Postgres database {self.db_name} clean done.")

        await self._migration_if_needed()

    # -- log connection info --

    async def log_connection_info(self):
        if self.db_pool is None:
            logger.warning(f"log_connection_info: Postgres database {self.db_name} pool is not initialized")
            return

        # get server connections
        async with self.get_db_connection() as conn:
            server_connections = await conn.fetchval("SELECT COUNT(*) FROM pg_stat_activity;")
            server_max_connections = await conn.fetchval(
                "SELECT setting FROM pg_settings WHERE name=$1;", "max_connections"
            )

        # get client connections
        client_connections = self.db_pool.get_size()
        max_client_connections = self.db_pool.get_max_size()

        logger.info(
            f"db[{self.db_name}]: "
            f"client pool size = {client_connections}/{max_client_connections}, "
            f"server connections = {server_connections}/{server_max_connections}"
        )

    # -- health check --
    async def health_check(self) -> bool:
        """Check if postgres database is healthy"""
        if self.db_pool is None:
            logger.error("Postgres health check failed: db pool is not initialized")
            return False

        try:
            async with self.get_db_connection() as conn:
                await conn.fetchval("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Postgres[{self.db_name}]] health check failed: error={e}")
            return False
