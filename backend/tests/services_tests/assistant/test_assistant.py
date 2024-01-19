import pytest

from tests.services_api.assistant.assistant import (create_assistant, get_assistant, list_assistants, update_assistant,
                                                    delete_assistant)
from tests.services_api.model.model import create_model
from tests.services_tests.assistant import Assistant
from tests.settings import OPENAI_API_KEY


class TestAssistant(Assistant):

    data_list = ['object', 'assistant_id', 'model_id',  'name', 'description',  "system_prompt_template", "memory",
                 'metadata', "tools",  "retrievals", "retrieval_configs", 'updated_timestamp', 'created_timestamp', ]
    data_keys = set(data_list)
    data_memory = ["type", "max_tokens", "max_messages"]
    data_memory_keys = set(data_memory)
    data_retrieval_configs = ["top_k", "method", "max_tokens"]
    data_retrieval_configs_keys = set(data_retrieval_configs)

    @pytest.mark.run(order=51)
    @pytest.mark.asyncio
    async def test_create_assistant(self):

        create_chat_completion_model_data = {
            "model_schema_id": "openai/gpt-3.5-turbo",
            "name": "My Language Model",
            "credentials": {"OPENAI_API_KEY": OPENAI_API_KEY}
        }

        create_chat_completion_model_res = await create_model(create_chat_completion_model_data)
        create_chat_completion_model_res_json = create_chat_completion_model_res.json()
        Assistant.chat_completion_model_id = create_chat_completion_model_res_json.get("data").get("model_id")

        create_assistant_data = {

                "model_id": Assistant.chat_completion_model_id,
                "name": "My Assistant",
                "description": "A helpful assistant",
                "system_prompt_template": [
                    "You are a professional assistant speaking {{language}}."
                ],
                "memory": {
                    "type": "naive"
                },
                "tools": [],
                "retrievals": [],
                "retrieval_configs": {
                    "top_k": 3,
                    "method": "memory"
                },
                "metadata": {}
            }

        res = await create_assistant(create_assistant_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        for key in create_assistant_data:
            assert res_json.get("data").get(key) == create_assistant_data[key]
        assert set(res_json.get("data").keys()) == self.data_keys
        assert (set(res_json.get("data").get("memory").keys()).issubset(self.data_memory_keys))
        assert (set(res_json.get("data").get("retrieval_configs").keys()).issubset(self.data_retrieval_configs_keys))
        Assistant.assistant_id = res_json.get("data").get("assistant_id")
        Assistant.assistant_name = res_json.get("data").get("name")

    @pytest.mark.run(order=52)
    @pytest.mark.asyncio
    async def test_get_assistant(self):

        get_res = await get_assistant(Assistant.assistant_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 200
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("assistant_id") == Assistant.assistant_id
        assert set(get_res_json.get("data").keys()) == self.data_keys
        assert (set(get_res_json.get("data").get("memory").keys()).issubset(self.data_memory_keys))
        assert (set(get_res_json.get("data").get("retrieval_configs").keys()).
                issubset(self.data_retrieval_configs_keys))

    @pytest.mark.run(order=53)
    @pytest.mark.asyncio
    async def test_list_assistants(self):

        list_assistants_data = {
            "limit": 10,
            "offset": 0,
            "order": "desc",
            "id_search": Assistant.assistant_id[:5],
            "name_search": Assistant.assistant_name[:5],
        }
        res = await list_assistants(list_assistants_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert len(res_json.get("data")) == 1
        assert res_json.get("fetched_count") == 1
        assert res_json.get("total_count") == 1
        assert res_json.get("has_more") is False

    @pytest.mark.run(order=54)
    @pytest.mark.asyncio
    async def test_update_assistant(self):

        update_assistant_data = {

                "model_id": Assistant.chat_completion_model_id,
                "name": "My Assistant",
                "description": "A helpful assistant",
                "system_prompt_template": [
                    "You are a professional assistant speaking {{language}}."
                ],
                "memory": {
                    "type": "zero"
                },
                "tools": [],
                "retrievals": [],
                "retrieval_configs": {
                    "top_k": 3,
                    "method": "memory"
                },
                "metadata": {}
            }
        res = await update_assistant(Assistant.assistant_id, update_assistant_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("assistant_id") == Assistant.assistant_id
        for key in update_assistant_data:
            assert res_json.get("data").get(key) == update_assistant_data[key]
        assert set(res_json.get("data").keys()) == self.data_keys
        assert (set(res_json.get("data").get("memory").keys()).issubset(self.data_memory_keys))
        assert (set(res_json.get("data").get("retrieval_configs").keys()).issubset(self.data_retrieval_configs_keys))

    @pytest.mark.run(order=80)
    @pytest.mark.asyncio
    async def test_delete_assistant(self):

        res = await delete_assistant(Assistant.assistant_id)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
