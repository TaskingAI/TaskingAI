import os

from .utils.utils import generate_test_cases

import aiohttp
import pytest


@pytest.mark.parametrize("test_data", generate_test_cases(), ids=lambda d: d["id"])
@pytest.mark.asyncio
async def test_plugins(test_data):
    bundle_id = test_data["id"].split("/")[0]
    plugin_id = test_data["id"].split("/")[1]
    if bundle_id == "stability_ai" or plugin_id == "internet_search_4_02_16k":
        pytest.skip("Skipping test as bundle_id is not provided")
    output_schema = test_data["output_schema"]
    bundle_credentials = test_data["bundle_credentials"]
    mode = test_data["mode"]
    input_params = test_data["input"]
    output = test_data["output"]

    bundle_credentials = {credential: os.environ.get(credential) for credential in bundle_credentials}

    async with aiohttp.ClientSession() as session:
        request_data = {
            "bundle_id": bundle_id,
            "plugin_id": plugin_id,
            "input_params": input_params,
            "credentials": bundle_credentials,
            "project_id": "test_project_id",
        }

        error_data_to_print = {
            "bundle_id": bundle_id,
            "plugin_id": plugin_id,
            "input_params": input_params,
            "credentials": {
                credential: bundle_credentials.get(credential, "NOT FOUND")[:4] for credential in bundle_credentials
            },
        }
        async with session.post("http://localhost:8000/v1/execute", json=request_data) as response:
            result = await response.json()
            if mode == "schema":
                assert result["status"] == "success", f"test failed, request = {error_data_to_print}, result = {result}"
                assert (
                    result["data"]["status"] == 200
                ), f"test failed, request = {error_data_to_print}, result = {result}"
                for key in output_schema:
                    assert (
                        key in result["data"]["data"]
                    ), f"test failed, request = {error_data_to_print}, result = {result}"

            if mode == "precise":
                assert result["status"] == "success", f"test failed, request = {error_data_to_print}, result = {result}"
                for key in output:
                    assert (
                        result["data"]["data"][key] == output[key]
                    ), f"test failed, request = {error_data_to_print}, result = {result}"
