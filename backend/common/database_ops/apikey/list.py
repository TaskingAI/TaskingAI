from common.models import Apikey


async def get_apikey_total(
    conn,
):
    row = await conn.fetchrow(
        """
        SELECT COUNT(*) FROM apikey
    """
    )
    return row["count"]


async def list_apikeys(
    conn,
):
    rows = await conn.fetch(
        f"""
         SELECT * FROM apikey
         ORDER BY created_timestamp desc
     """
    )
    apikeys = [Apikey.build(row) for row in rows]
    return apikeys
