from enum import Enum
from fastapi import HTTPException


class ErrorCode(str, Enum):
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    OBJECT_NOT_FOUND = "OBJECT_NOT_FOUND"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"
    REQUEST_VALIDATION_ERROR = "REQUEST_VALIDATION_ERROR"
    DATA_MODEL_VALIDATION_ERROR = "DATA_MODEL_VALIDATION_ERROR"
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
        "message": "Object does not exist.",
    },
    ErrorCode.TOO_MANY_REQUESTS: {
        "status_code": 429,
        "message": "Too many requests.",
    },
    ErrorCode.REQUEST_VALIDATION_ERROR: {
        "status_code": 422,
        "message": "Request validation error.",
    },
    ErrorCode.DATA_MODEL_VALIDATION_ERROR: {
        "status_code": 400,
        "message": "Data model validation error.",
    },
    ErrorCode.PROVIDER_ERROR: {
        "status_code": 400,
        "message": "Provider api responds error.",
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
    raise_http_error(ErrorCode.PROVIDER_ERROR, "Error on calling provider model API: " + provider_error_message)
