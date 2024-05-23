import pytest
import json
from backend.tests.api_services.assistant.chat import create_chat, get_chat, list_chats, update_chat, delete_chat
from backend.tests.services_tests.assistant import Assistant
from backend.tests.common.config import CONFIG


@pytest.mark.api_test
class TestChat(Assistant):

    @pytest.mark.run(order=191)
    @pytest.mark.asyncio
    async def test_create_chat(self):

        create_chat_data_list = [
            {
              "name": "assistant_chat",
        },
            {
                "metadata": {"yyy": "yyy"},
            }]
        for index, create_chat_data in enumerate(create_chat_data_list):
            res = await create_chat(Assistant.assistant_id, create_chat_data)

            assert res.status_code == 200,  res.json()
            assert res.json().get("status") == "success"
            for key in create_chat_data:
                assert res.json().get("data").get(key) == create_chat_data[key]
            assert res.json().get("data").get("assistant_id") == Assistant.assistant_id

            Assistant.chat_id = res.json().get("data").get("chat_id")

            get_res = await get_chat(Assistant.assistant_id, Assistant.chat_id)
            assert get_res.status_code == 200,  get_res.json()
            assert get_res.json().get("status") == "success"
            assert get_res.json().get("data").get("chat_id") == Assistant.chat_id
            assert get_res.json().get("data").get("assistant_id") == Assistant.assistant_id
            for key in create_chat_data:
                assert get_res.json().get("data").get(key) == create_chat_data[key]


    @pytest.mark.run(order=192)
    @pytest.mark.asyncio
    async def test_get_chat(self):
        res = await get_chat(Assistant.assistant_id, Assistant.chat_id)

        assert res.status_code == 200,  res.json()
        assert res.json().get("status") == "success"
        assert res.json().get("data").get("chat_id") == Assistant.chat_id
        assert res.json().get("data").get("assistant_id") == Assistant.assistant_id


    @pytest.mark.run(order=193)
    @pytest.mark.asyncio
    async def test_list_chats(self):
        list_chats_data = {
            "limit": 10,
            "order": "desc",
            "after": Assistant.chat_id,
        }
        res = await list_chats(Assistant.assistant_id, list_chats_data)
        assert res.status_code == 200,  res.json()
        assert res.json().get("status") == "success"
        assert len(res.json().get("data")) == 1
        assert res.json().get("fetched_count") == 1
        assert res.json().get("has_more") is False


    @pytest.mark.run(order=194)
    @pytest.mark.asyncio
    async def test_update_chat(self):

        update_chat_data_list = [
            {
              "metadata": {"xxx": "xxx"},
        },
            {
                "name": "update_chat_name",
            }
        ]
        for update_chat_data in update_chat_data_list:
            res = await update_chat(Assistant.assistant_id, Assistant.chat_id, update_chat_data)

            assert res.status_code == 200,  res.json()
            assert res.json().get("status") == "success"
            assert res.json().get("data").get("chat_id") == Assistant.chat_id
            assert res.json().get("data").get("assistant_id") == Assistant.assistant_id

            for key in update_chat_data:
                assert res.json().get("data").get(key) == update_chat_data[key]

            get_res = await get_chat(Assistant.assistant_id, Assistant.chat_id)
            assert get_res.status_code == 200,  get_res.json()
            assert get_res.json().get("status") == "success"
            assert get_res.json().get("data").get("chat_id") == Assistant.chat_id
            assert get_res.json().get("data").get("assistant_id") == Assistant.assistant_id
            for key in update_chat_data:
                assert get_res.json().get("data").get(key) == update_chat_data[key]


    @pytest.mark.run(order=209)
    @pytest.mark.asyncio
    async def test_delete_chat(self):

        chats_res = await list_chats(Assistant.assistant_id, {"limit": 100})
        chat_ids = [chat.get("chat_id") for chat in chats_res.json().get("data")]
        for chat_id in chat_ids:

            res = await delete_chat(Assistant.assistant_id, chat_id)
            res_json = res.json()
            assert res.status_code == 200,  res.json()
            assert res_json.get("status") == "success"

            get_res = await get_chat(Assistant.assistant_id, chat_id)
            get_res_json = get_res.json()
            assert get_res.status_code == 404, get_res.json()
            assert get_res_json.get("status") == "error"
            assert get_res_json.get("error").get("code") == "OBJECT_NOT_FOUND"
