import pytest

from backend.tests.api_services.apikey.apikey import create_apikey, list_apikey, get_apikey, update_apikey, delete_apikey
from backend.tests.common.config import CONFIG


@pytest.mark.web_test
class TestApikey:

    apikey_id: str = None

    @pytest.mark.asyncio
    @pytest.mark.run(order=101)
    async def test_create_apikey(self):

        create_apikey_data = {"name": "test_apikey"}
        res = await create_apikey(create_apikey_data)
        res_json = res.json()

        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("name") == create_apikey_data["name"]
        assert "*" in res_json.get("data").get("apikey")

        TestApikey.apikey_id = res_json.get("data").get("apikey_id")

        get_res = await get_apikey(TestApikey.apikey_id, {})
        get_res_json = get_res.json()
        assert get_res.status_code == 200,  get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("apikey_id") == TestApikey.apikey_id
        assert get_res_json.get("data").get("name") == create_apikey_data["name"]
        assert "*" in get_res_json.get("data").get("apikey")

    @pytest.mark.asyncio
    @pytest.mark.run(order=102)
    async def test_list_apikey(self):

        res = await list_apikey()
        res_json = res.json()

        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        assert len(res_json.get("data")) == res_json.get("fetched_count") >= 1
        assert res_json.get("has_more") is False


    @pytest.mark.asyncio
    @pytest.mark.run(order=103)
    async def test_get_apikey(self):

        get_apikey_data = {"plain": "True"}
        res = await get_apikey(TestApikey.apikey_id, get_apikey_data)
        res_json = res.json()

        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("apikey_id") == TestApikey.apikey_id
        assert "*" not in res_json.get("data").get("apikey")


    @pytest.mark.asyncio
    @pytest.mark.run(order=104)
    async def test_update_apikey(self):

        update_apikey_data = {"name": "test_apikey_update"}
        res = await update_apikey(TestApikey.apikey_id, update_apikey_data)
        res_json = res.json()

        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("apikey_id") == TestApikey.apikey_id
        assert res_json.get("data").get("name") == update_apikey_data["name"]
        assert "*" in res_json.get("data").get("apikey")

        get_res = await get_apikey(TestApikey.apikey_id, {})
        get_res_json = get_res.json()
        assert get_res.status_code == 200,  get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("apikey_id") == TestApikey.apikey_id
        assert get_res_json.get("data").get("name") == update_apikey_data["name"]
        assert "*" in get_res_json.get("data").get("apikey")


    @pytest.mark.asyncio
    @pytest.mark.run(order=105)
    async def test_delete_apikey(self):
        res = await delete_apikey(TestApikey.apikey_id)
        res_json = res.json()

        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"

        get_res = await get_apikey(TestApikey.apikey_id, {})
        get_res_json = get_res.json()
        assert get_res.status_code == 404, get_res.json()
        assert get_res_json.get("status") == "error"
        assert get_res_json.get("error").get("code") == "OBJECT_NOT_FOUND"
