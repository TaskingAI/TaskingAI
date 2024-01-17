import pytest

from tests.services_api.model.provider import list_providers, get_provider


class TestProvider:

    provider_list = ["object", "provider_id", "name", "credentials_schema"]
    provider_keys = set(provider_list)
    provider_credentials_schema_list = ["type", "properties", "required", "additionalProperties"]
    provider_credentials_schema_keys = set(provider_credentials_schema_list)

    @pytest.mark.asyncio
    @pytest.mark.run(order=21)
    async def test_list_providers(self):

        res = await list_providers()
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert len(res_json.get("data")) == 5
        assert res_json.get("fetched_count") == 5
        assert res_json.get("total_count") == 5
        assert res_json.get("has_more") is False

    @pytest.mark.asyncio
    @pytest.mark.run(order=22)
    async def test_get_provider(self):

        params = {"provider_id": "openai"}
        res = await get_provider(params)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        for provider in res_json.get("data"):
            assert provider.get("provider_id") == params["provider_id"]
            assert set(provider.keys()) == self.provider_keys
            assert set(provider.get("credentials_schema").keys()) == self.provider_credentials_schema_keys
