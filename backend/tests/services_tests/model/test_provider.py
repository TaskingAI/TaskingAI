import pytest

from tests.services_api.model.provider import list_providers


class TestProvider:

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
