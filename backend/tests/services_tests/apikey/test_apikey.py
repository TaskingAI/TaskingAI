import pytest

from tests.services_api.apikey.apikey import create_apikey, list_apikeys, get_apikey, update_apikey, delete_apikey


class TestApikey:

    apikey_list = ["object", "apikey_id", "apikey", "name", "created_timestamp", "updated_timestamp"]
    apikey_keys = set(apikey_list)
    apikey_id = None

    @pytest.mark.asyncio
    @pytest.mark.run(order=11)
    async def test_create_apikey(self):

        create_apikey_data = {"name": "test_apikey"}
        res = await create_apikey(create_apikey_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("name") == create_apikey_data["name"]
        assert set(res_json.get("data").keys()) == self.apikey_keys
        TestApikey.apikey_id = res_json.get("data").get("apikey_id")

    @pytest.mark.asyncio
    @pytest.mark.run(order=12)
    async def test_list_apikeys(self):

        res = await list_apikeys()
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("total_count") >= len(res_json.get("data")) == res_json.get("fetched_count") >= 1
        assert res_json.get("has_more") is False or True

    @pytest.mark.asyncio
    @pytest.mark.run(order=13)
    async def test_get_apikey(self):

        get_apikey_data = {"plain": "True"}
        res = await get_apikey(TestApikey.apikey_id, get_apikey_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("apikey_id") == TestApikey.apikey_id
        assert "*" not in res_json.get("data").get("apikey")
        assert set(res_json.get("data").keys()) == self.apikey_keys

    @pytest.mark.asyncio
    @pytest.mark.run(order=14)
    async def test_update_apikey(self):

        update_apikey_data = {"name": "test_apikey_update"}
        res = await update_apikey(TestApikey.apikey_id, update_apikey_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("apikey_id") == TestApikey.apikey_id
        assert res_json.get("data").get("name") == update_apikey_data["name"]
        assert "*" in res_json.get("data").get("apikey")
        assert set(res_json.get("data").keys()) == self.apikey_keys

    @pytest.mark.asyncio
    @pytest.mark.run(order=15)
    async def test_delete_apikey(self):

        res = await delete_apikey(TestApikey.apikey_id)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
