import asyncio
import pytest

from backend.tests.api_services.admin.admin import login, verify_token, refresh_token, logout
from backend.tests.common.config import CONFIG


@pytest.mark.web_test
class TestAdmin:


    @pytest.mark.asyncio
    @pytest.mark.run(order=91)
    async def test_login(self):

        login_data = {"username": CONFIG.DEFAULT_ADMIN_USERNAME, "password": CONFIG.DEFAULT_ADMIN_PASSWORD}
        res = await login(login_data)
        res_json = res.json()
        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("username") == CONFIG.DEFAULT_ADMIN_USERNAME
        CONFIG.Authentication = res_json.get("data").get("token")

    @pytest.mark.run(order=92)
    @pytest.mark.asyncio
    async def test_verify_token(self):

        res = await verify_token(CONFIG.Authentication)
        res_json = res.json()
        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        await asyncio.sleep(1)

    @pytest.mark.run(order=93)
    @pytest.mark.asyncio
    async def test_refresh_token(self):

        res = await refresh_token(CONFIG.Authentication)
        res_json = res.json()
        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("token") != CONFIG.Authentication

        # verify token with old token

        verify_old_token_res = await verify_token(CONFIG.Authentication)
        assert verify_old_token_res.status_code == 401
        assert verify_old_token_res.json().get("status") == "error"
        assert verify_old_token_res.json().get("error").get("code") == "TOKEN_VALIDATION_FAILED"

        # verify token with new token

        CONFIG.Authentication = res_json.get("data").get("token")
        verify_new_token_res = await verify_token(CONFIG.Authentication)
        verify_new_token_res_json = verify_new_token_res.json()
        assert verify_new_token_res.status_code == 200,  res.json()
        assert verify_new_token_res_json.get("status") == "success"

    @pytest.mark.run(order=999)
    @pytest.mark.asyncio
    async def test_logout(self):

        res = await logout(CONFIG.Authentication)
        res_json = res.json()
        assert res.status_code == 200,  res.json()
        assert res_json.get("status") == "success"

        # verify token with old token

        verify_old_token_res = await verify_token(CONFIG.Authentication)
        assert verify_old_token_res.status_code == 401
        assert verify_old_token_res.json().get("status") == "error"
        assert verify_old_token_res.json().get("error").get("code") == "TOKEN_VALIDATION_FAILED"
