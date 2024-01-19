from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from .error_code import ErrorCode, error_messages
import traceback
from config import CONFIG

router = APIRouter()


def build_error_response_dict(error_code, message: str = None, debug: str = None):
    error_dict = {
        "code": error_code.value if isinstance(error_code, ErrorCode) else str(error_code),
        "message": error_messages[error_code]["message"] if message is None else message,
    }
    if debug:
        error_dict["debug"] = debug
    return {"status": "error", "error": error_dict}


async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=build_error_response_dict(
                error_code=exc.detail.get("error_code", exc.detail.get("code", ErrorCode.UNKNOWN_ERROR)),
                message=exc.detail.get("message", None),
            ),
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content=build_error_response_dict(ErrorCode.UNKNOWN_ERROR, message=str(exc.detail)),
        )


async def custom_request_validation_error_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    locs_list = [str(loc) for loc in errors[0]["loc"]]
    location = "/".join(locs_list)
    message = location + ": " + exc.errors()[0]["msg"]
    debug = str(exc.errors()[0])
    return JSONResponse(
        status_code=422,
        content=build_error_response_dict(error_code=ErrorCode.REQUEST_VALIDATION_ERROR, message=message, debug=debug),
    )


async def custom_validation_error_handler(request: Request, exc: ValidationError):
    detail_str = str(exc.errors()[0])
    return JSONResponse(
        status_code=422,
        content=build_error_response_dict(error_code=ErrorCode.DATA_MODEL_VALIDATION_ERROR, message=detail_str),
    )


async def custom_exception_handler(request: Request, exc: Exception):
    detail_str = str(exc)
    debug_str = None
    if CONFIG.TEST or CONFIG.DEV:
        debug_str = "Traceback: " + "".join(traceback.format_tb(exc.__traceback__))

    return JSONResponse(
        status_code=500,
        content=build_error_response_dict(
            error_code=ErrorCode.INTERNAL_SERVER_ERROR, message=detail_str, debug=debug_str
        ),
    )
