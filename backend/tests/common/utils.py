import requests
from typing import Dict

from tests.settings import HOST, WEB_SERVICE_PORT
from app.config import CONFIG


class ResponseWrapper:
    def __init__(self, status: int, json_data: Dict):
        self.status_code = status
        self._json_data = json_data

    def json(self):
        return self._json_data


def get_headers(token):
    return {"Authorization": "Bearer " + token}


def get_token():
    app_base_url = f"{HOST}:{WEB_SERVICE_PORT}{CONFIG.WEB_ROUTE_PREFIX}"
    login_data = {"username": CONFIG.DEFAULT_ADMIN_USERNAME, "password": CONFIG.DEFAULT_ADMIN_PASSWORD}
    response = requests.post(f"{app_base_url}/admins/login", json=login_data)
    return response.json()["data"]["token"]


Token = get_token()


def get_apikey():
    app_base_url = f"{HOST}:{WEB_SERVICE_PORT}{CONFIG.WEB_ROUTE_PREFIX}"
    create_apikey_res = requests.post(
        f"{app_base_url}/apikeys", headers=get_headers(Token), json={"name": "test_apikey"}
    )
    apikey_id = create_apikey_res.json()["data"]["apikey_id"]
    apikey_res = requests.get(f"{app_base_url}/apikeys/{apikey_id}", headers=get_headers(Token), params={"plain": True})
    return apikey_res.json()["data"]["apikey"]


if CONFIG.API:
    APIKEY = get_apikey()
