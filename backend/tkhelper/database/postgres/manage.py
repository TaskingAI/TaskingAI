from typing import List
import logging

logger = logging.Logger(__name__)


async def clean_data(conn, table_name_order: List[str]):
    """
    Clean data in db_postgres.

    :param conn: asyncpg connection object
    :param table_name_order: list of table name prefixes in the order they should be dropped
    """

    try:
        # Clearing and reinitializing db_postgres
        # Implement detailed cleanup steps for tables, sequences, functions, etc.

        # Drop all tables
        tables = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname='public';")
        table_names = [table["tablename"] for table in tables]

        for prefix in table_name_order:
            current_table_names = [table_name for table_name in table_names if table_name.startswith(prefix)]
            table_names = [table_name for table_name in table_names if table_name not in current_table_names]
            for table_name in current_table_names:
                await conn.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")

        for table_name in table_names:
            await conn.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")

        # Drop all extensions
        extensions = await conn.fetch("""SELECT extname FROM pg_extension;""")
        for extension in extensions:
            ext_name = extension["extname"]
            await conn.execute(f'DROP EXTENSION IF EXISTS "{ext_name}" CASCADE;')

        # Drop all sequences
        sequences = await conn.fetch(
            "SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema='public';"
        )
        for sequence in sequences:
            seq_name = sequence["sequence_name"]
            await conn.execute(f"DROP SEQUENCE IF EXISTS {seq_name} CASCADE;")

        # Drop all functions
        functions = await conn.fetch(
            "SELECT routine_name FROM information_schema.routines "
            "WHERE specific_schema='public' AND type_udt_name!='trigger';"
        )
        for function in functions:
            func_name = function["routine_name"]
            await conn.execute(f"DROP FUNCTION IF EXISTS {func_name} CASCADE;")

        await conn.execute("CREATE LANGUAGE plpgsql;")

        logger.info("Database cleaned and reinitialized successfully.")
    except Exception as e:
        logger.error(f"Error during database cleanup: {e}")
