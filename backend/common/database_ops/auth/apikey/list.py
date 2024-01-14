from common.models import Apikey, SortOrderEnum, ListResult
from common.database_ops.utils import get_object_total, list_objects


async def get_apikey_total(
    postgres_conn,
) -> int:
    return await get_object_total(conn=postgres_conn, table_name="apikey")


async def list_apikeys(
    postgres_conn,
) -> ListResult:
    """
    List apikeys
    :param postgres_conn: postgres connection
    :return: a list of apikeys, total count of apikeys, and whether there are more apikeys
    """

    return await list_objects(
        conn=postgres_conn,
        object_class=Apikey,
        table_name="apikey",
        order=SortOrderEnum.DESC,
        sort_field="created_timestamp",
    )
