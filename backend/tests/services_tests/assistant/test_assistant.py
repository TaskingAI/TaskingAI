import json

import pytest

from backend.tests.api_services.assistant.assistant import (
    create_assistant,
    get_assistant,
    list_assistants,
    update_assistant,
    delete_assistant,
    get_ui_assistant,
    list_ui_assistants,
)
from backend.tests.services_tests.assistant import Assistant
from backend.tests.services_tests.retrieval import Retrieval
from backend.tests.services_tests.tool import Tool
from backend.tests.common.config import CONFIG


@pytest.mark.api_test
class TestAssistant(Assistant):

    @pytest.mark.run(order=181)
    @pytest.mark.asyncio
    async def test_create_assistant(self):

        create_assistant_data_list = [
            {
                "model_id": CONFIG.chat_completion_model_id,
                "memory": {"type": "zero"},
                "retrieval_configs": {"top_k": 3, "method": "memory"},
            },
            {
                "model_id": CONFIG.chat_completion_model_id,
                "name": "My Assistant",
                "description": "A helpful assistant",
                "system_prompt_template": ["You are a professional assistant speaking {{language}}."],
                "memory": {"type": "naive"},
                "tools": [
                    {
                        "type": "plugin",
                        "id": "open_weather/get_current_weather",
                    },
                    {
                        "type": "action",
                        "id": Tool.action_id,
                    },
                ],
                "retrievals": [
                    {
                        "type": "collection",
                        "id": Retrieval.collection_id,
                    }
                ],
                "retrieval_configs": {"top_k": 3, "method": "memory", "max_tokens": 1000, "score_threshold": 0.5},
                "metadata": {"create": "create"},
            },
        ]
        for index, create_assistant_data in enumerate(create_assistant_data_list):
            res = await create_assistant(create_assistant_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            for key in create_assistant_data:
                if key == "memory":
                    for memory_key in create_assistant_data[key]:
                        assert (
                            res_json.get("data").get(key).get(memory_key) == create_assistant_data[key][memory_key]
                        )
                elif key == "retrieval_configs":
                    for retrieval_configs_key in create_assistant_data[key]:
                        assert (
                            res_json.get("data").get(key).get(retrieval_configs_key)
                            == create_assistant_data[key][retrieval_configs_key]
                        )
                else:
                    assert res_json.get("data").get(key) == create_assistant_data[key]

            Assistant.assistant_id = res_json.get("data").get("assistant_id")
            Assistant.assistant_name = res_json.get("data").get("name")
            Assistant.assistant_ids.append(Assistant.assistant_id)

            get_res = await get_assistant(Assistant.assistant_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 200, get_res.json()
            assert get_res_json.get("status") == "success"
            assert get_res_json.get("data").get("assistant_id") == Assistant.assistant_id

            for key in create_assistant_data:
                if key == "memory":
                    for memory_key in create_assistant_data[key]:
                        assert (
                            res_json.get("data").get(key).get(memory_key) == create_assistant_data[key][memory_key]
                        )
                elif key == "retrieval_configs":
                    for retrieval_configs_key in create_assistant_data[key]:
                        assert (
                            res_json.get("data").get(key).get(retrieval_configs_key)
                            == create_assistant_data[key][retrieval_configs_key]
                        )
                else:
                    assert get_res_json.get("data").get(key) == create_assistant_data[key]

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    async def test_get_assistant(self):

        get_res = await get_assistant(Assistant.assistant_id)
        get_res_json = get_res.json()

        assert get_res.status_code == 200, get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("assistant_id") == Assistant.assistant_id

    @pytest.mark.run(order=182)
    @pytest.mark.asyncio
    async def test_get_ui_assistant(self):
        if "WEB" in CONFIG.TEST_MODE:

            get_res = await get_ui_assistant(Assistant.assistant_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 200, get_res.json()
            assert get_res_json.get("status") == "success"
            assert get_res_json.get("data").get("assistant_id") == Assistant.assistant_id
            assert get_res_json.get("data").get("retrievals")[0].get("name") == "test_update"
            assert get_res_json.get("data").get("tools")[0].get("name") == "Open Weather / Get current weather data"
            assert get_res_json.get("data").get("tools")[1].get("name") == "get_current_weather"
            assert get_res_json.get("data").get("model_name") == "My Chat Completion Model Test"

    @pytest.mark.run(order=183)
    @pytest.mark.asyncio
    async def test_list_assistants(self):

        list_assistants_data_list = [
            {"limit": 10, "order": "desc", "after": Assistant.assistant_id},
            {"prefix_filter": json.dumps({"assistant_id": Assistant.assistant_id[:10]})},
            {"prefix_filter": json.dumps({"name": Assistant.assistant_name[:5]})},
        ]
        for list_assistants_data in list_assistants_data_list:
            if "API" in CONFIG.TEST_MODE:
                if list_assistants_data.get("prefix_filter"):
                    list_assistants_data.pop("prefix_filter")
            if list_assistants_data == {}:
                continue
            res = await list_assistants(list_assistants_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            assert len(res_json.get("data")) == 1
            assert res_json.get("fetched_count") == 1
            assert res_json.get("has_more") is False
            if list_assistants_data.get("prefix_filter"):
                prefix_filter_dict = json.loads(list_assistants_data.get("prefix_filter"))
                for key in prefix_filter_dict:
                    assert res_json.get("data")[0].get(key).startswith(prefix_filter_dict.get(key))

    @pytest.mark.run(order=183)
    @pytest.mark.asyncio
    async def test_list_ui_assistants(self):

        if "WEB" in CONFIG.TEST_MODE:

            list_ui_assistants_data_list = [
                {"limit": 10, "order": "asc", "before": Assistant.assistant_id},
                {"prefix_filter": json.dumps({"assistant_id": Assistant.assistant_id[:10]})},
                {"prefix_filter": json.dumps({"name": Assistant.assistant_name[:5]})},
            ]
            for list_ui_assistants_data in list_ui_assistants_data_list:
                res = await list_ui_assistants(list_ui_assistants_data)
                res_json = res.json()
                assert res.status_code == 200, res.json()
                assert res_json.get("status") == "success"
                assert len(res_json.get("data")) == 1
                assert res_json.get("fetched_count") == 1
                assert res_json.get("has_more") is False
                if list_ui_assistants_data.get("prefix_filter"):
                    prefix_filter_dict = json.loads(list_ui_assistants_data.get("prefix_filter"))
                    for key in prefix_filter_dict:
                        assert res_json.get("data")[0].get(key).startswith(prefix_filter_dict.get(key))
                    assert res_json.get("data")[0].get("retrievals")[0].get("name") == "test_update"
                    assert (
                            res_json.get("data")[0].get("tools")[0].get("name")
                            == "Open Weather / Get current weather data"
                    )
                    assert res_json.get("data")[0].get("tools")[1].get("name") == "get_current_weather"
                    assert res_json.get("data")[0].get("model_name") == "My Chat Completion Model Test"

    @pytest.mark.run(order=184)
    @pytest.mark.asyncio
    async def test_update_assistant(self):

        update_assistant_data = {
            "model_id": CONFIG.chat_completion_model_id,
            "name": "My Assistant",
            "description": "A helpful assistant",
            "system_prompt_template": ["You are a professional assistant speaking {{language}}."],
            "memory": {"type": "zero"},
            "tools": [
                {
                    "type": "plugin",
                    "id": "open_weather/get_current_weather",
                },
                {
                    "type": "action",
                    "id": Tool.action_id,
                },
            ],
            "retrievals": [
                {
                    "type": "collection",
                    "id": Retrieval.collection_id,
                }
            ],
            "retrieval_configs": {"top_k": 3, "method": "memory", "max_tokens": 500, "score_threshold": 0.8},
            "metadata": {"update": "update"},
        }
        res = await update_assistant(Assistant.assistant_id, update_assistant_data)
        res_json = res.json()

        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("assistant_id") == Assistant.assistant_id
        for key in update_assistant_data:
            if key == "memory":
                for memory_key in update_assistant_data[key]:
                    assert res_json.get("data").get(key).get(memory_key) == update_assistant_data[key][memory_key]
            elif key == "retrieval_configs":
                for retrieval_configs_key in update_assistant_data[key]:
                    assert (
                        res_json.get("data").get(key).get(retrieval_configs_key)
                        == update_assistant_data[key][retrieval_configs_key]
                    )
            else:
                assert res_json.get("data").get(key) == update_assistant_data[key]

        get_res = await get_assistant(Assistant.assistant_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 200, get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("assistant_id") == Assistant.assistant_id
        for key in update_assistant_data:
            if key == "memory":
                for memory_key in update_assistant_data[key]:
                    assert res_json.get("data").get(key).get(memory_key) == update_assistant_data[key][memory_key]
            elif key == "retrieval_configs":
                for retrieval_configs_key in update_assistant_data[key]:
                    assert (
                        res_json.get("data").get(key).get(retrieval_configs_key)
                        == update_assistant_data[key][retrieval_configs_key]
                    )
            else:
                assert get_res_json.get("data").get(key) == update_assistant_data[key]

    @pytest.mark.run(order=210)
    @pytest.mark.asyncio
    async def test_delete_assistant(self):
        assistants = await list_assistants({"limit": 100})
        assistant_ids = [assistant.get("assistant_id") for assistant in assistants.json().get("data")]
        for assistant_id in assistant_ids:
            res = await delete_assistant(assistant_id)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"

            get_res = await get_assistant(assistant_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 404, get_res.json()
            assert get_res_json.get("status") == "error"
            assert get_res_json.get("error").get("code") == "OBJECT_NOT_FOUND"
