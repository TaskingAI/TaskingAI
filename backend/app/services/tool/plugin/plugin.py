import json
from typing import Dict, List
import aiohttp
from aiohttp.client_exceptions import ClientResponseError

from tkhelper.utils import ResponseWrapper

from app.models import BundleInstance
from app.config import CONFIG
from app.operators import bundle_instance_ops

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

    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                f"{CONFIG.TASKINGAI_PLUGIN_URL}/v1/execute",
                json={
                    "bundle_id": bundle_instance.bundle_id,
                    "plugin_id": plugin_id,
                    "input_params": parameters,
                    "encrypted_credentials": bundle_instance.encrypted_credentials,
                    "project_id": "taskingai"
                },
            )

            bytes_read = 0
            max_size = 64 * 1024
            data_chunks = []

            # check the size of the response
            async for chunk in response.content.iter_any():
                bytes_read += len(chunk)
                if bytes_read > max_size:
                    raise ClientResponseError(
                        response.request_info, response.history, message="Response too large", status=response.status
                    )
                data_chunks.append(chunk)

            data_bytes = b"".join(data_chunks)
            try:
                # Assuming the response is JSON and decode here
                data_dict = json.loads(data_bytes.decode("utf-8"))
            except json.JSONDecodeError:
                # Handle non-JSON response or decode error
                return {"status": 500, "data": {"error": "Failed to decode the plugin response"}}

            response_wrapper = ResponseWrapper(response.status, data_dict)

            if response.status == 200:
                data = response_wrapper.json().get("data")
                return {"status": data["status"], "data": data["data"]}

            return {"status": response.status, "data": response_wrapper.json().get("error")}

    except ClientResponseError as e:
        if "Response too large" in e.message:
            return {
                "status": e.status,
                "data": {"error": f"Response data is too large. Maximum character length is {max_size}."},
            }
        else:
            return {"status": e.status, "data": {"error": f"API call failed with status {e.status}"}}

    except Exception as e:
        return {"status": 500, "data": {"error": "Failed to execute the plugin"}}


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
