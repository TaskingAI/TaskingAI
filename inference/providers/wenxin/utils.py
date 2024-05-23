from provider_dependency.chat_completion import ProviderCredentials
import datetime
from datetime import datetime, timedelta
from threading import Lock
import requests
from app.error import raise_http_error, ErrorCode
from typing import Dict, Tuple

__all__ = ["generate_access_token"]

# Global access token cache
baidu_access_tokens: Dict[str, "BaiduAccessToken"] = {}
baidu_access_tokens_lock = Lock()


class BaiduAccessToken:
    """Represents a Baidu access token."""

    def __init__(self, api_key: str, access_token: str, expires_in: int) -> None:
        self.api_key = api_key
        self.access_token = access_token
        self.expires = datetime.now() + timedelta(seconds=expires_in)


def request_access_token(api_key: str, secret_key: str) -> Tuple[str, int]:
    """Request an access token from Baidu."""
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": api_key, "client_secret": secret_key}
    headers = {"Accept": "application/json"}

    try:
        response = requests.post(url, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()
        if "error" in result:
            raise_http_error(ErrorCode.PROVIDER_ERROR, f"Failed to get access token from Baidu: {result}")
        return result["access_token"], result.get("expires_in", 2592000)
    except requests.exceptions.RequestException as e:
        raise_http_error(ErrorCode.PROVIDER_ERROR, f"Failed to get access token from Baidu: {e}")


def generate_access_token(credentials: ProviderCredentials) -> BaiduAccessToken:
    """Get or refresh a Baidu access token from cache or by requesting a new one."""
    api_key = credentials.WENXIN_API_KEY
    secret_key = credentials.WENXIN_SECRET_KEY
    with baidu_access_tokens_lock:
        now = datetime.now()
        baidu_access_tokens.update({k: v for k, v in baidu_access_tokens.items() if v.expires > now})

        if api_key not in baidu_access_tokens:
            token_str, _ = request_access_token(api_key, secret_key)
            # Set custom expiration period of 7 days instead of using Baidu's expires_in (default 30 days)
            expires_in_seconds = 7 * 24 * 60 * 60
            token = BaiduAccessToken(api_key, token_str, expires_in_seconds)
            baidu_access_tokens[api_key] = token
        return baidu_access_tokens[api_key]
