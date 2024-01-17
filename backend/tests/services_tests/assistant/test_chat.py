import pytest

from tests.services_api.assistant.chat import create_chat, get_chat, list_chats, update_chat, delete_chat
from tests.services_tests.assistant import Assistant


class TestChat(Assistant):

    data_list = ['object', 'chat_id', 'assistant_id',  'metadata', "memory", 'created_timestamp', 'updated_timestamp']
    data_keys = set(data_list)
    data_memory = ["type", "messages", "max_messages", "max_tokens"]
    data_content_keys = set(data_memory)

    @pytest.mark.run(order=61)
    @pytest.mark.asyncio
    async def test_create_chat(self):

        create_chat_data = {
              "metadata": {"xxx": "xxx"}
        }
        res = await create_chat(Assistant.assistant_id, create_chat_data)
        assert res.status_code == 200
        assert res.json().get("status") == "success"
        for key in create_chat_data:
            assert res.json().get("data").get(key) == create_chat_data[key]
        assert res.json().get("data").get("assistant_id") == Assistant.assistant_id
        assert set(res.json().get("data").keys()) == self.data_keys
        assert (set(res.json().get("data").get("memory").keys()).issubset(self.data_content_keys))
        Assistant.chat_id = res.json().get("data").get("chat_id")

    @pytest.mark.run(order=62)
    @pytest.mark.asyncio
    async def test_get_chat(self):

        res = await get_chat(Assistant.assistant_id, Assistant.chat_id)
        assert res.status_code == 200
        assert res.json().get("status") == "success"
        assert res.json().get("data").get("chat_id") == Assistant.chat_id
        assert res.json().get("data").get("assistant_id") == Assistant.assistant_id
        assert set(res.json().get("data").keys()) == self.data_keys
        assert (set(res.json().get("data").get("memory").keys()).issubset(self.data_content_keys))

    @pytest.mark.run(order=63)
    @pytest.mark.asyncio
    async def test_list_chats(self):

        list_chats_data = {
            "limit": 10,
            "offset": 0,
            "order": "desc",
            "id_search": Assistant.chat_id[:5]
        }
        res = await list_chats(Assistant.assistant_id, list_chats_data)
        assert res.status_code == 200
        assert res.json().get("status") == "success"
        assert len(res.json().get("data")) == 1
        assert res.json().get("fetched_count") == 1
        assert res.json().get("total_count") == 1
        assert res.json().get("has_more") is False

    @pytest.mark.run(order=64)
    @pytest.mark.asyncio
    async def test_update_chat(self):

        update_chat_data = {
              "metadata": {"xxx": "xxx"}
        }
        res = await update_chat(Assistant.assistant_id, Assistant.chat_id, update_chat_data)
        assert res.status_code == 200
        assert res.json().get("status") == "success"
        assert res.json().get("data").get("chat_id") == Assistant.chat_id
        assert res.json().get("data").get("assistant_id") == Assistant.assistant_id
        assert set(res.json().get("data").keys()) == self.data_keys
        assert (set(res.json().get("data").get("memory").keys()).issubset(self.data_content_keys))
        for key in update_chat_data:
            assert res.json().get("data").get(key) == update_chat_data[key]

    @pytest.mark.run(order=78)
    @pytest.mark.asyncio
    async def test_delete_chat(self):

        res = await delete_chat(Assistant.assistant_id, Assistant.chat_id)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
