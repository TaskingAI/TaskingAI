import jwt
import time
from app.models import ProviderCredentials
from app.error import raise_http_error, ErrorCode


def generate_token(access_key: str, secret_key: str, exp_seconds: int, nbf_seconds: int):
    try:
        payload = {
            "iss": access_key,
            "exp": int(time.time()) + exp_seconds,
            "nbf": int(time.time()) - nbf_seconds,
        }

        token = jwt.encode(payload, secret_key, headers={"alg": "HS256", "typ": "JWT"})
        return token
    except Exception as e:
        raise_http_error(ErrorCode.CREDENTIALS_VALIDATION_ERROR, "Invalid Access Key or Secret Key")


def build_sensetime_header(credentials: ProviderCredentials):
    exp_seconds = 1800
    nbf_seconds = 5
    # use API_KEY to generate JWT token for Sensetime
    token = generate_token(
        credentials.SENSETIME_ACCESS_KEY_ID, credentials.SENSETIME_SECRET_ACCESS_KEY, exp_seconds, nbf_seconds
    )
    return {
        "Authorization": f"Bearer {token}",
    }
