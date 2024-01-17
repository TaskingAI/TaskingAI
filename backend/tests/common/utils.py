import requests
from typing import Dict

from tests.config import HOST
from config import CONFIG


class ResponseWrapper:
    def __init__(self, status: int, json_data: Dict):
        self.status_code = status
        self._json_data = json_data

    def json(self):
        return self._json_data


def get_headers(token):
    return {"Authorization": "Bearer " + token}


def get_token():

    app_base_url = f"{HOST}:{CONFIG.SERVICE_PORT}{CONFIG.APP_ROUTE_PREFIX}"
    login_data = {"username": CONFIG.DEFAULT_ADMIN_USERNAME, "password": CONFIG.DEFAULT_ADMIN_PASSWORD}
    response = requests.post(f"{app_base_url}/admins/login", json=login_data)
    return response.json()['data']['token']


Token = get_token()
