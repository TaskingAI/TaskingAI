import pytest

from backend.tests.api_services.assistant.assistant import (create_assistant, get_assistant, list_assistants, update_assistant,
                                                     delete_assistant)
from backend.tests.api_services.assistant.chat import create_chat, get_chat, list_chats, update_chat, delete_chat
from backend.tests.api_services.assistant.message import (create_message, get_message, list_messages, update_message,
                                                    generate_message)
from backend.tests.services_tests.assistant import Assistant
from backend.tests.common.config import CONFIG


@pytest.mark.api_test
class TestMessage(Assistant):


    @pytest.mark.run(order=201)
    @pytest.mark.asyncio
    async def test_create_message(self):

        create_message_data_list = [
            {
                "role": "user",
                "content": {
                    "text": "hello, can you help me?"
                }
            },
            {
                "role": "user",
                "content": {
                    "text": "what is the meaning of 123?"
                },
                "metadata": {
                    "x": "x"
                }
            }
        ]
        for index, create_message_data in enumerate(create_message_data_list):
            res = await create_message(Assistant.assistant_id, Assistant.chat_id, create_message_data)

            assert res.status_code == 200,  res.json()
            assert res.json().get("status") == "success"
            for key in create_message_data:
                assert res.json().get("data").get(key) == create_message_data[key]
            assert res.json().get("data").get("chat_id") == Assistant.chat_id
            assert res.json().get("data").get("assistant_id") == Assistant.assistant_id

            Assistant.message_id = res.json().get("data").get("message_id")

            get_res = await get_message(Assistant.assistant_id, Assistant.chat_id, Assistant.message_id)
            assert get_res.status_code == 200,  get_res.json()
            assert get_res.json().get("status") == "success"
            assert get_res.json().get("data").get("message_id") == Assistant.message_id
            assert get_res.json().get("data").get("chat_id") == Assistant.chat_id
            assert get_res.json().get("data").get("assistant_id") == Assistant.assistant_id
            for key in create_message_data:
                assert get_res.json().get("data").get(key) == create_message_data[key]


    @pytest.mark.run(order=202)
    @pytest.mark.asyncio
    async def test_list_messages(self):

        list_messages_data = {
            "limit": 10,
            "order": "asc",
            "before": Assistant.message_id
        }
        res = await list_messages(Assistant.assistant_id, Assistant.chat_id, list_messages_data)
        assert res.status_code == 200,  res.json()
        assert res.json().get("status") == "success"
        assert len(res.json().get("data")) == 1
        assert res.json().get("fetched_count") == 1
        assert res.json().get("has_more") is False


    @pytest.mark.run(order=203)
    @pytest.mark.asyncio
    async def test_get_message(self):
        res = await get_message(Assistant.assistant_id, Assistant.chat_id, Assistant.message_id)
        res_json = res.json()

        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("message_id") == Assistant.message_id
        assert res_json.get("data").get("chat_id") == Assistant.chat_id
        assert res_json.get("data").get("assistant_id") == Assistant.assistant_id

    @pytest.mark.run(order=204)
    @pytest.mark.asyncio
    async def test_update_message(self):

        update_message_data = {
            "metadata": {"xxx": "xxx"}
        }
        res = await update_message(Assistant.assistant_id, Assistant.chat_id, Assistant.message_id,
                                   update_message_data)

        assert res.status_code == 200,  res.json()
        assert res.json().get("status") == "success"
        assert res.json().get("data").get("message_id") == Assistant.message_id
        assert res.json().get("data").get("chat_id") == Assistant.chat_id
        assert res.json().get("data").get("assistant_id") == Assistant.assistant_id

        for key in update_message_data:
            assert res.json().get("data").get(key) == update_message_data[key]

        get_res = await get_message(Assistant.assistant_id, Assistant.chat_id, Assistant.message_id)
        assert get_res.status_code == 200,  get_res.json()
        assert get_res.json().get("status") == "success"
        assert get_res.json().get("data").get("message_id") == Assistant.message_id
        assert get_res.json().get("data").get("chat_id") == Assistant.chat_id
        assert get_res.json().get("data").get("assistant_id") == Assistant.assistant_id

        for key in update_message_data:
            assert get_res.json().get("data").get(key) == update_message_data[key]


    @pytest.mark.run(order=205)
    @pytest.mark.asyncio
    async def test_generate_message(self):
        res = await generate_message(Assistant.assistant_id, Assistant.chat_id, {})
        res_json = res.json()

        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("chat_id") == Assistant.chat_id
        assert res_json.get("data").get("assistant_id") == Assistant.assistant_id

        assert res_json.get("data").get("role") == "assistant"
        assert res_json.get("data").get("content").get("text") is not None
