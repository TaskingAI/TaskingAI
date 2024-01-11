from common.error import raise_http_error, ErrorCode
from starlette.requests import Request

from fastapi import HTTPException


def check_http_error(response):
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", {}))


async def project_id_required(request: Request) -> str:
    values = list(request.path_params.values())
    if len(values) > 0:
        # check if project_id is valid
        project_id = values[0]
        if len(project_id) != 8:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Project ID is not valid")

        return project_id
