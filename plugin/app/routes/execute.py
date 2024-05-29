import logging

from fastapi import APIRouter
from typing import Any, Dict, Union, Optional
from pydantic import BaseModel, Field, model_validator

from app.error import raise_http_error, ErrorCode, TKHttpException
from app.cache import get_plugin_handler, get_plugin
from app.models import (
    validate_bundle_credentials,
    BundleCredentials,
    PluginInput,
    PluginOutput,
    PluginHandler,
)

router = APIRouter()
logger = logging.getLogger(__name__)


class RunToolRequest(BaseModel):
    project_id: Optional[str] = Field(None, description="The project id.")

    bundle_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The bundle id.",
        examples=["bundle_1"],
    )
    plugin_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The plugin id.",
        examples=["plugin_1"],
    )
    input_params: Dict = Field(
        {},
        description="The input parameters of the plugin.",
        examples=[
            {
                "input_1": "value_1",
                "input_2": "value_2",
            }
        ],
    )
    credentials: BundleCredentials = Field(
        ...,
        description="The credentials of the model provider.",
        examples=[{"API_KEY": "YOUR_API_KEY"}],
    )

    @model_validator(mode="before")
    def validate_before(cls, data: Any):

        # validate bundle credentials
        credentials = validate_bundle_credentials(data)
        data["credentials"] = credentials
        data.pop("encrypted_credentials", None)

        return data

    @model_validator(mode="after")
    def validate_after(cls, data: Any):

        # validate plugin_id
        plugin = get_plugin(
            bundle_id=data.bundle_id,
            plugin_id=data.plugin_id,
        )

        if not plugin:
            raise_http_error(ErrorCode.OBJECT_NOT_FOUND, "Plugin not found")

        # validate input_params
        plugin.validate_input(data.input_params)

        return data


class RunToolResponse(BaseModel):
    status: str = Field(
        "success",
        Literal="success",
        description="The status of the response.",
    )
    data: PluginOutput = Field(
        ...,
        description="The data of the response.",
    )


class BaseDataResponse(BaseModel):
    status: str = Field("success", Literal="success", description="The status of the response.")
    data: Any = Field(...)


@router.post(
    "/execute",
    operation_id="execute_plugin",
    summary="Execute a plugin.",
    tags=["Plugin"],
    responses={422: {"description": "Unprocessable Entity"}},
    response_model=Union[RunToolResponse, BaseDataResponse],
)
async def api_execute(
    data: RunToolRequest,
):
    plugin: PluginHandler = get_plugin_handler(
        bundle_id=data.bundle_id,
        plugin_id=data.plugin_id,
    )
    if not plugin:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, f"Plugin {data.plugin_id} not found")

    cleaned_dict = {k: v for k, v in data.input_params.items() if v is not None}
    data.input_params = cleaned_dict

    try:
        plugin_output = await plugin.execute(
            credentials=data.credentials,
            plugin_input=PluginInput(input_params=data.input_params, project_id=data.project_id),
        )
    except TKHttpException as e:
        logger.error(f"api_execute: {data.bundle_id}/{data.plugin_id}. Input params: {data.input_params}. Error: {e}")
        return BaseDataResponse(
            data={
                "status": e.status_code,
                "data": {
                    "error": e.detail.get("message", "Error when handling response from provider"),
                },
            }
        )
    except Exception as e:
        raise_http_error(ErrorCode.INTERNAL_SERVER_ERROR, str(e))

    return RunToolResponse(
        data=plugin_output,
    )
