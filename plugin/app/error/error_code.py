from enum import Enum
from fastapi import HTTPException


class ErrorCode(str, Enum):
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    OBJECT_NOT_FOUND = "OBJECT_NOT_FOUND"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"
    REQUEST_VALIDATION_ERROR = "REQUEST_VALIDATION_ERROR"
    PROVIDER_ERROR = "PROVIDER_ERROR"
    CREDENTIALS_VALIDATION_ERROR = "CREDENTIALS_VALIDATION_ERROR"


class HttpError:
    http_code: int
    error_code: ErrorCode
    message: str


error_messages = {
    ErrorCode.UNKNOWN_ERROR: {
        "status_code": 500,
        "message": "Unknown error occurred.",
    },
    ErrorCode.INTERNAL_SERVER_ERROR: {
        "status_code": 500,
        "message": "Internal server error.",
    },
    ErrorCode.OBJECT_NOT_FOUND: {
        "status_code": 404,
        "message": "Object not found.",
    },
    ErrorCode.TOO_MANY_REQUESTS: {
        "status_code": 429,
        "message": "Too many requests.",
    },
    ErrorCode.REQUEST_VALIDATION_ERROR: {
        "status_code": 422,
        "message": "Request validation error.",
    },
    ErrorCode.PROVIDER_ERROR: {
        "status_code": 500,
        "message": "Error on calling provider API.",
    },
    ErrorCode.CREDENTIALS_VALIDATION_ERROR: {
        "status_code": 401,
        "message": "Credentials validation error.",
    },
}

assert len(error_messages) == len(ErrorCode)


class TKHttpException(HTTPException):
    pass


def error_message(message: str, code: ErrorCode):
    return {
        "object": "Error",
        "code": code,
        "message": message,
    }


def raise_http_error(error_code: ErrorCode, message: str):
    raise TKHttpException(
        status_code=error_messages[error_code]["status_code"],
        detail={"error_code": error_code, "message": message},
    )


def raise_provider_api_error(provider_error_message: str):
    error_code = ErrorCode.PROVIDER_ERROR
    if not provider_error_message:
        provider_error_message = "Error on calling provider API."
    raise TKHttpException(
        status_code=error_messages[error_code]["status_code"],
        detail={"error_code": error_code, "message": provider_error_message},
    )


def raise_credentials_validation_error(message: str = None):
    error_code = ErrorCode.CREDENTIALS_VALIDATION_ERROR
    if not message:
        message = (
            "Bundle credentials validation has failed. Please check whether your credentials are correct "
            "and if you have enough quota with the provider."
        )
    raise TKHttpException(
        status_code=error_messages[error_code]["status_code"],
        detail={"error_code": error_code, "message": message},
    )
