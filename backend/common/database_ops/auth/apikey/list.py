from common.database.postgres.pool import postgres_db_pool
from common.models import Apikey, SortOrderEnum, ListResult
from common.database_ops.utils import get_object_total, list_objects


async def get_apikey_total() -> int:
    async with postgres_db_pool.get_db_connection() as conn:
        return await get_object_total(conn, table_name="apikey")


async def list_apikeys() -> ListResult:
    """
    List apikeys
    :return: a list of apikeys, total count of apikeys, and whether there are more apikeys
    """
    async with postgres_db_pool.get_db_connection() as conn:
        return await list_objects(
            conn=conn,
            object_class=Apikey,
            table_name="apikey",
            order=SortOrderEnum.DESC,
            sort_field="created_timestamp",
            object_id_name="apikey_id",
        )
