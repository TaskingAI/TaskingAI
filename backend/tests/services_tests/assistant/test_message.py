import pytest

from tests.services_api.assistant.message import (create_message, get_message, list_messages, update_message,
                                                  generate_message)
from tests.services_tests.assistant import Assistant


class TestMessage(Assistant):

    data_list = ['object', "message_id", 'chat_id', 'assistant_id', "role", 'metadata', "content", 'created_timestamp',
                 'updated_timestamp']
    data_keys = set(data_list)

    @pytest.mark.run(order=66)
    @pytest.mark.asyncio
    async def test_create_message(self):

        create_message_data = {
                                "role": "user",
                                "content": {

                                     "text": "what is the meaning of 123?"


                                    },
                                "metadata": {
                                    "x": "x"
                                            }
                                }
        res = await create_message(Assistant.assistant_id, Assistant.chat_id, create_message_data)
        assert res.status_code == 200
        assert res.json().get("status") == "success"
        for key in create_message_data:
            assert res.json().get("data").get(key) == create_message_data[key]
        assert res.json().get("data").get("chat_id") == Assistant.chat_id
        assert res.json().get("data").get("assistant_id") == Assistant.assistant_id
        assert set(res.json().get("data").keys()) == self.data_keys
        Assistant.message_id = res.json().get("data").get("message_id")

    @pytest.mark.run(order=67)
    @pytest.mark.asyncio
    async def test_list_messages(self):

        list_messages_data = {
            "limit": 10,
            "order": "desc"
        }
        res = await list_messages(Assistant.assistant_id, Assistant.chat_id, list_messages_data)
        assert res.status_code == 200
        assert res.json().get("status") == "success"
        assert res.json().get("fetched_count") == 1
        assert res.json().get("total_count") == 1
        assert res.json().get("has_more") is False

    @pytest.mark.run(order=68)
    @pytest.mark.asyncio
    async def test_get_message(self):

        res = await get_message(Assistant.assistant_id, Assistant.chat_id, Assistant.message_id)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("message_id") == Assistant.message_id
        assert res_json.get("data").get("chat_id") == Assistant.chat_id
        assert res_json.get("data").get("assistant_id") == Assistant.assistant_id
        assert set(res_json.get("data").keys()) == self.data_keys

    @pytest.mark.run(order=69)
    @pytest.mark.asyncio
    async def test_update_message(self):

        update_message_data = {
            "metadata": {"xxx": "xxx"}
        }
        res = await update_message(Assistant.assistant_id, Assistant.chat_id, Assistant.message_id, update_message_data)
        assert res.status_code == 200
        assert res.json().get("status") == "success"
        assert res.json().get("data").get("message_id") == Assistant.message_id
        assert res.json().get("data").get("chat_id") == Assistant.chat_id
        assert res.json().get("data").get("assistant_id") == Assistant.assistant_id
        assert set(res.json().get("data").keys()) == self.data_keys
        for key in update_message_data:
            assert res.json().get("data").get(key) == update_message_data[key]

    @pytest.mark.run(order=70)
    @pytest.mark.asyncio
    async def test_generate_message(self):

        res = await generate_message(Assistant.assistant_id, Assistant.chat_id, {})
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("chat_id") == Assistant.chat_id
        assert res_json.get("data").get("assistant_id") == Assistant.assistant_id
        assert set(res_json.get("data").keys()).issubset(self.data_keys)
        assert res_json.get("data").get("role") == "assistant"
        assert res_json.get("data").get("content").get("text") is not None
