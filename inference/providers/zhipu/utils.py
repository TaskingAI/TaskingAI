import jwt
import time
from app.models import ProviderCredentials
from app.error import raise_http_error, ErrorCode


def generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise_http_error(ErrorCode.CREDENTIALS_VALIDATION_ERROR, "Invalid API Key")

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


def build_zhipu_header(credentials: ProviderCredentials):
    exp_seconds = 1800
    # use API_KEY to generate JWT token for zhipu
    token = generate_token(credentials.ZHIPU_API_KEY, exp_seconds)
    return {
        "Authorization": f"Bearer {token}",
    }
