import pytest

from tests.services_api.model.model import create_model, list_models, get_model, update_model, delete_model
from tests.settings import OPENAI_API_KEY


class TestModel:

    model_id = None
    model_list = ["object", "model_id", "model_schema_id", "provider_id", "provider_model_id", "name", "type",
                  "updated_timestamp", "created_timestamp",  "display_credentials", 'properties']
    model_keys = set(model_list)
    create_model_list = [
        {
            "name": "My Text Embedding Model",
            "model_schema_id": "openai/text-embedding-ada-002",
            "credentials": {"OPENAI_API_KEY": OPENAI_API_KEY}
        },
        {
            "name": "My Chat Completion Model",
            "model_schema_id": "openai/gpt-3.5-turbo",
            "credentials": {"OPENAI_API_KEY": OPENAI_API_KEY}
        }
    ]

    update_model_list = [
        {
            "name": "My Chat Completion Model Test",
            "credentials": {"OPENAI_API_KEY": OPENAI_API_KEY}
        }
    ]

    @pytest.mark.run(order=22)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("create_model_data", create_model_list)
    async def test_create_model(self, create_model_data):

        res = await create_model(create_model_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("name") == create_model_data["name"]
        assert res_json.get("data").get("model_schema_id") == create_model_data["model_schema_id"]
        assert set(res_json.get("data").keys()) == self.model_keys
        TestModel.model_id = res_json.get("data").get("model_id")

    @pytest.mark.asyncio
    @pytest.mark.run(order=23)
    async def test_list_models(self):

        list_model_data = {
            "limit": 10,
            "offset": 0,
            "order": "asc",
            "id_search": self.model_id[:6],
            "name_search": "My",
            "provider_id": "openai",
            "type": "chat_completion",
        }

        res = await list_models(list_model_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert len(res_json.get("data")) == 1
        assert res_json.get("fetched_count") == 1
        assert res_json.get("total_count") == 1
        assert res_json.get("has_more") is False

    @pytest.mark.asyncio
    @pytest.mark.run(order=24)
    async def test_get_model(self):

        res = await get_model(TestModel.model_id)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("model_id") == TestModel.model_id
        assert set(res_json.get("data").keys()) == self.model_keys

    @pytest.mark.asyncio
    @pytest.mark.run(order=25)
    @pytest.mark.parametrize("update_model_data", update_model_list)
    async def test_update_model(self, update_model_data):

        res = await update_model(TestModel.model_id, update_model_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("model_id") == TestModel.model_id
        assert res_json.get("data").get("name") == update_model_data["name"]
        assert set(res_json.get("data").keys()) == self.model_keys

    @pytest.mark.asyncio
    @pytest.mark.run(order=26)
    async def test_delete_model(self):

        res = await delete_model(TestModel.model_id)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
