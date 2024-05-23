import pytest

from backend.tests.api_services.model.provider import list_providers, get_provider
from backend.tests.common.config import CONFIG

@pytest.mark.web_test
class TestProvider:


    @pytest.mark.asyncio
    @pytest.mark.run(order=111)
    async def test_list_providers(self):
        res = await list_providers({"limit": 100, "order": "asc", "type": "chat_completion"})
        res_json = res.json()

        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        assert len(res_json.get("data")) > 0
        total = len(res_json.get("data"))
        assert res_json.get("fetched_count") == total
        assert res_json.get("has_more") is False
        for provider in res_json.get("data"):
            assert "chat_completion" in provider.get("model_types") or "wildcard" in provider.get("model_types")


    @pytest.mark.asyncio
    @pytest.mark.run(order=112)
    async def test_get_provider(self):
        params = {"provider_id": "openai"}
        res = await get_provider(params)
        res_json = res.json()

        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        provider = res_json.get("data")
        assert provider.get("provider_id") == params["provider_id"]

