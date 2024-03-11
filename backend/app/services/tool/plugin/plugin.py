from typing import Dict, List
from app.models import BundleInstance
from app.operators import bundle_instance_ops
import aiohttp
from app.config import CONFIG
from tkhelper.utils import ResponseWrapper

__all__ = [
    "run_plugin",
    "get_bundle_registered_dict",
]


async def run_plugin(
    bundle_instance_id: str,
    plugin_id: str,
    parameters: Dict,
) -> Dict:
    """
    Run a plugin
    :param bundle_instance_id: the bundle ID
    :param plugin_id: the action ID
    :param parameters: the parameters for the API call
    :return: the response of the API call
    """
    bundle_instance: BundleInstance = await bundle_instance_ops.get(
        bundle_instance_id=bundle_instance_id,
    )

    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f"{CONFIG.TASKINGAI_PLUGIN_URL}/v1/execute",
            json={
                "bundle_id": bundle_instance.bundle_id,
                "plugin_id": plugin_id,
                "input_params": parameters,
                "encrypted_credentials": bundle_instance.encrypted_credentials,
            },
        )
        response_wrapper = ResponseWrapper(response.status, await response.json())
        if response.status == 200:
            data = response_wrapper.json().get("data")
            return {"status": data["status"], "data": data["data"]}

        return {"status": response.status, "data": response_wrapper.json().get("error")}


async def get_bundle_registered_dict(
    bundle_ids: List[str],
) -> Dict[str, bool]:
    """
    Check if the bundle is registered
    :param bundle_ids: the bundle IDs
    :return: a dict indicating if the bundle is registered
    """
    import asyncpg
    from app.database import postgres_pool

    async with postgres_pool.get_db_connection() as conn:
        # select the bundle instances
        query = """
        SELECT bundle_id
        FROM bundle_instance
        WHERE bundle_id = ANY($1)
        """
        try:
            rows = await conn.fetch(query, bundle_ids)
        except asyncpg.exceptions.UndefinedTableError:
            return {bundle_id: False for bundle_id in bundle_ids}

    # build the set of registered bundle IDs
    registered_bundle_ids = {row["bundle_id"] for row in rows}

    # check if the bundle is registered
    return {bundle_id: bundle_id in registered_bundle_ids for bundle_id in bundle_ids}
