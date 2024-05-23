import pytest
from test.inference_service.inference import *


class TestOthers:

    caches_keys_list = ["providers", "model_schemas", "i18n"]
    cache_checksums_keys_list = ["i18n_checksum", "model_schema_checksum", "provider_checksum"]
    white_resources_list = ["https://www.llama-api.com/account/usage"]

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_020")
    async def test_cache(self):
        result = await caches()
        assert result.status_code == 200, f"test_cache failed: result={result}"
        assert result.json()["status"] == "success"
        assert set(self.caches_keys_list).issubset(result.json()["data"].keys())

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_021")
    async def test_cache_checksums(self):
        result = await cache_checksums()
        assert result.status_code == 200, f"test_cache failed: result={result}"
        assert result.json()["status"] == "success"
        assert set(self.cache_checksums_keys_list).issubset(result.json()["data"].keys())

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_022")
    async def test_list_providers(self):
        result = await list_providers()
        assert result.status_code == 200, f"test_list_providers failed: result={result}"
        assert result.json()["status"] == "success"
        assert len(result.json()["data"]) > 0
        providers = result.json()["data"]
        for provider in providers:
            for key, value in provider["resources"].items():
                if key in ["official_credentials_url", "taskingai_documentation_url"]:
                    continue
                if value != "" and value not in self.white_resources_list:
                    get_result = await get_resources(value)
                    pytest.assume(get_result.status != 404, f"get_resources failed: result={get_result}")

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_022")
    async def test_get_provider(self):
        list_res = await list_providers()
        providers = list_res.json()["data"]
        for provider in providers:
            request_data = {"provider_id": provider["provider_id"]}
            result = await get_provider(request_data)
            assert result.status_code == 200, f"test_get_provider failed: result={result}"
            assert result.json()["status"] == "success"
            assert result.json()["data"][0]["provider_id"] == request_data["provider_id"]

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_024")
    async def test_get_provider_icon(self):
        list_res = await list_providers()
        providers = list_res.json()["data"]
        for provider in providers:
            provider_svg = provider["icon_svg_url"].split("/")[-1]
            result = await get_provider_icon(provider_svg)
            assert result.status == 200, f"test_get_provider_icon failed: result={result}"
            assert result.ok is True
            assert result.reason == "OK"

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_025")
    async def test_list_model_schemas(self):
        result = await list_model_schemas()
        assert result.status_code == 200, f"test_list_model_schemas failed: result={result}"
        assert result.json()["status"] == "success"
        assert len(result.json()["data"]) > 0

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_026")
    async def test_get_model_schema(self):
        list_res = await list_model_schemas()
        model_schemas = list_res.json()["data"]
        for model_schema in model_schemas:
            request_data = {"model_schema_id": model_schema["model_schema_id"]}
            result = await get_model_schema(request_data)
            assert result.status_code == 200, f"test_get_provider failed: result={result}"
            assert result.json()["status"] == "success"
            assert result.json()["data"][0]["model_schema_id"] == request_data["model_schema_id"]

    @pytest.mark.asyncio
    @pytest.mark.test_id("inference_027")
    async def test_get_model_properties_schema(self):
        result = await model_property_schemas()
        assert result.status_code == 200, f"test_get_provider failed: result={result}"
        assert result.json()["status"] == "success"
