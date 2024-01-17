import pytest

from tests.services_api.model.model_schemas import list_model_schemas


class TestModelSchemas:

    @pytest.mark.asyncio
    @pytest.mark.run(order=21)
    async def test_list_model_schemas(self):

        list_model_schemas_data = {"limit": 10, "offset": 0, "provider_id": "openai", "type": "chat_completion"}
        res = await list_model_schemas(list_model_schemas_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert len(res_json.get("data")) == 4
        assert res_json.get("fetched_count") == 4
        assert res_json.get("total_count") == 4
        assert res_json.get("has_more") is False
