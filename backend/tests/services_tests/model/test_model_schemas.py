import pytest

from tests.services_api.model.model_schemas import list_model_schemas, get_model_schema


class TestModelSchemas:

    model_schema_list = ["object",  "model_schema_id", "name", "description", "provider_id", "provider_model_id",
                         "type", "properties"]
    model_schema_keys = set(model_schema_list)

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

    @pytest.mark.asyncio
    @pytest.mark.run(order=22)
    async def test_get_model_schema(self):

        params = {"model_schema_id": "openai/text-embedding-ada-002"}
        res = await get_model_schema(params)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        for model_schema in res_json.get("data"):
            assert model_schema.get("model_schema_id") == params["model_schema_id"]
            assert set(model_schema.keys()) == self.model_schema_keys
