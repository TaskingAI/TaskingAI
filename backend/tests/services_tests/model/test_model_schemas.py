import pytest

from backend.tests.api_services.model.model_schemas import list_model_schemas, get_model_schema
from backend.tests.common.config import CONFIG


@pytest.mark.web_test
class TestModelSchemas:


    model_schema_id = "openai/gpt-3.5-turbo"

    @pytest.mark.asyncio
    @pytest.mark.run(order=111)
    async def test_list_model_schemas(self):

        list_model_schemas_data = {"limit": 30, "offset": 0, "provider_id": "openai", "type": "chat_completion"}
        res = await list_model_schemas(list_model_schemas_data)
        res_json = res.json()

        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert len(res_json.get("data")) == res_json.get("fetched_count") > 0
        assert res_json.get("has_more") is False
        for model_schema in res_json.get("data"):
            assert model_schema.get("provider_id") == list_model_schemas_data["provider_id"]
            assert model_schema.get("type") in ["chat_completion", "wildcard"]
        TestModelSchemas.model_schema_id = res_json.get("data")[0]["model_schema_id"]


    @pytest.mark.asyncio
    @pytest.mark.run(order=112)
    async def test_get_model_schema(self):

        params = {"model_schema_id": TestModelSchemas.model_schema_id}
        res = await get_model_schema(params)
        res_json = res.json()

        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        model_schema = res_json.get("data")
        assert model_schema.get("model_schema_id") == params["model_schema_id"]
