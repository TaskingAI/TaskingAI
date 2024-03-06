import asyncio
import pytest

from tests.services_api.admin.admin import login, verify_token, refresh_token, logout
from app.config import CONFIG


class TestAdmin:
    admin_list = ["object", "admin_id", "username", "token", "created_timestamp", "updated_timestamp"]
    admin_keys = set(admin_list)
    token = None

    @pytest.mark.asyncio
    @pytest.mark.run(order=101)
    async def test_login(self):
        login_data = {"username": CONFIG.DEFAULT_ADMIN_USERNAME, "password": CONFIG.DEFAULT_ADMIN_PASSWORD}
        res = await login(login_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("username") == CONFIG.DEFAULT_ADMIN_USERNAME
        assert set(res_json.get("data").keys()) == self.admin_keys
        TestAdmin.token = res_json.get("data").get("token")

    @pytest.mark.run(order=102)
    @pytest.mark.asyncio
    async def test_verify_token(self):
        res = await verify_token(TestAdmin.token)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        await asyncio.sleep(1)

    @pytest.mark.run(order=103)
    @pytest.mark.asyncio
    async def test_refresh_token(self):
        res = await refresh_token(TestAdmin.token)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("token") != TestAdmin.token
        assert set(res_json.get("data").keys()) == self.admin_keys

        # verify token with old token

        verify_old_token_res = await verify_token(TestAdmin.token)
        assert verify_old_token_res.status_code == 401
        assert verify_old_token_res.json().get("status") == "error"
        assert verify_old_token_res.json().get("error").get("code") == "TOKEN_VALIDATION_FAILED"

        # verify token with new token

        TestAdmin.token = res_json.get("data").get("token")
        verify_new_token_res = await verify_token(TestAdmin.token)
        verify_new_token_res_json = verify_new_token_res.json()
        assert verify_new_token_res.status_code == 200
        assert verify_new_token_res_json.get("status") == "success"

    @pytest.mark.run(order=104)
    @pytest.mark.asyncio
    async def test_logout(self):
        res = await logout(TestAdmin.token)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"

        # verify token with old token

        verify_old_token_res = await verify_token(TestAdmin.token)
        assert verify_old_token_res.status_code == 401
        assert verify_old_token_res.json().get("status") == "error"
        assert verify_old_token_res.json().get("error").get("code") == "TOKEN_VALIDATION_FAILED"
