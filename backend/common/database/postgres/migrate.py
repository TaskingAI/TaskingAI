import os
import re
from common.database.redis.connection import redis_pool
import logging

logger = logging.Logger(__name__)

MIGRATION_TABLE = "migration_version"


async def create_migration_table(
    conn,
):
    """
    Create migration table if not exists

    :param conn: asyncpg database connection
    """
    try:
        await conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {MIGRATION_TABLE} (
                version INTEGER PRIMARY KEY
            );
        """
        )
    except Exception as e:
        logger.error(f"Error creating migration table: {e}")


async def get_current_version(
    conn,
):
    """
    Get current migration version
    :param conn: asyncpg database connection
    :return: current migration version, if not exists, return 0
    """
    try:
        await create_migration_table(conn)
        result = await conn.fetchval(f"SELECT MAX(version) FROM {MIGRATION_TABLE}")
        return result or 0
    except Exception as e:
        logger.error(f"Error fetching current version: {e}")
        return 0


async def apply_migration(
    conn,
    version: int,
    sql: str,
):
    """
    Apply migration script to database
    :param conn: asyncpg database connection
    :param version: the target version of migration
    :param sql: sql script content
    """

    try:
        async with conn.transaction():
            if sql.strip() == "":
                logger.warning(f"Migration version {version} script is empty")
            else:
                await conn.execute(sql)
            await conn.execute(f"INSERT INTO {MIGRATION_TABLE} (version) VALUES ($1)", version)
            logger.info(f"Migration version {version} applied successfully")
    except Exception as e:
        logger.error(f"Error applying migration version {version}: {e}")


def extract_version_from_filename(
    migration_script_filename_format: str,
    filename: str,
):
    """
    Extract version from migration script filename
    :param filename: migration script filename
    :return: version number of the script
    """
    match = re.match(migration_script_filename_format, filename)
    return int(match.group(1)) if match else None


async def migrate_if_needed(
    conn,
    db_name: str,
    latest_version: int,
    migration_script_dir: str,
    migration_script_filename_format: str,
):
    current_version = await get_current_version(conn)
    if current_version >= latest_version:
        logger.info(f"Database {db_name} is already up to date with version {current_version}")
        return

    logger.info(f"Init database {db_name} with version {current_version}")
    script_folder = os.path.join(os.path.dirname(__file__), migration_script_dir)
    migration_files = sorted(os.listdir(script_folder))

    version = current_version
    for filename in migration_files:
        version = extract_version_from_filename(migration_script_filename_format, filename)
        if version and version > current_version:
            filepath = os.path.join(script_folder, filename)
            with open(filepath, "r") as f:
                sql_content = f.read()
            await apply_migration(conn, version, sql_content)

    if version > current_version:
        logger.info(f"Database {db_name} upgraded to version {version}, target version is {latest_version}")
        await redis_pool.clean_data()
