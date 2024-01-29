import os
from typing import Dict
from common.models import Authentication, AuthenticationType, ActionMethod, ActionBodyType, ActionParam
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
import logging
import urllib.parse

logger = logging.getLogger(__name__)


def _prepare_headers(authentication: Authentication, extra_headers: Dict) -> Dict:
    """
    Prepares the headers for an HTTP request including authentication and additional headers.

    :param authentication: An Authentication object containing the authentication details.
    :param extra_headers: A dictionary of additional headers to include in the request.
    :return: A dictionary of headers for the HTTP request.
    """

    headers = {}

    if extra_headers:
        headers.update(extra_headers)

    if authentication:
        if authentication.type == AuthenticationType.basic:
            # Basic Authentication: Assume the secret is a base64 encoded string
            headers["Authorization"] = f"Basic {authentication.secret}"

        elif authentication.type == AuthenticationType.bearer:
            # Bearer Authentication: Add the secret as a bearer token
            headers["Authorization"] = f"Bearer {authentication.secret}"

        elif authentication.type == AuthenticationType.custom:
            # Custom Authentication: Return the custom content as headers
            headers.update(authentication.content)

    return headers


def _process_parameters(schema: Dict[str, ActionParam], parameters: Dict) -> Dict:
    """
    Processes parameters based on their schema and provided values.

    :param schema: A dictionary representing the parameter schema.
    :param parameters: A dictionary of provided parameter values.
    :return: A dictionary of processed parameters.
    """
    processed_params = {}
    for param_name, action_param in schema.items():
        param_value = None
        # Check for the presence of 'enum' in the parameter schema
        if action_param.is_single_value_enum():
            param_value = action_param.enum[0]
        elif param_name in parameters:
            param_value = parameters[param_name]

        if param_value is not None:
            processed_params[param_name] = param_value

        # todo: check if required
        # if action_param.required and param_value is None:
        #     raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message=f"Missing required parameter {param_name}")

    return processed_params


async def call_action_api(
    url: str,
    method: ActionMethod,
    path_param_schema: Dict[str, ActionParam],
    query_param_schema: Dict[str, ActionParam],
    body_type: ActionBodyType,
    body_param_schema: Dict[str, ActionParam],
    parameters: Dict,
    headers: Dict,
    authentication: Authentication,
) -> Dict:
    """
    Call an API according to OpenAPI schema.
    :param url: the URL of the API call
    :param method: the method of the API call
    :param path_param_schema: the path parameters schema
    :param query_param_schema: the query parameters schema
    :param body_type: the body type
    :param body_param_schema: the body parameters schema
    :param parameters: the parameters input by the user
    :param headers: the extra headers to be included in the API call
    :param authentication: the authentication of the action
    :return: Response from the API call
    """

    # Update URL with path parameters

    if path_param_schema:
        path_params = _process_parameters(path_param_schema, parameters)
        for param_name, param_value in path_params.items():
            url = url.replace(f"{{{param_name}}}", urllib.parse.quote(str(param_value)))

    # Prepare query parameters
    query_params = {}
    if query_param_schema:
        query_params = _process_parameters(query_param_schema, parameters)
        # cast boolean values to string
        for param_name, param_value in query_params.items():
            if isinstance(param_value, bool):
                query_params[param_name] = str(param_value).lower()

    # Prepare body
    body = None
    if body_type != ActionBodyType.NONE:
        body = _process_parameters(body_param_schema, parameters)

    # Prepare headers
    prepared_headers = _prepare_headers(authentication, headers)

    # Making the API call
    try:
        async with aiohttp.ClientSession() as session:
            request_kwargs = {"headers": prepared_headers}

            if query_params:
                request_kwargs["params"] = query_params

            if os.environ.get("HTTP_PROXY_URL"):
                request_kwargs["proxy"] = os.environ.get("HTTP_PROXY_URL")

            if body_type == ActionBodyType.JSON:
                request_kwargs["json"] = body
                prepared_headers["Content-Type"] = "application/json"
            elif body_type == ActionBodyType.FORM:
                request_kwargs["data"] = body
                prepared_headers["Content-Type"] = "application/x-www-form-urlencoded"

            logger.debug(f"call_action_api url={url} request kwargs: {request_kwargs}")

            async with session.request(method.value, url, **request_kwargs) as response:
                response_content_type = response.headers.get("Content-Type", "").lower()
                if "application/json" in response_content_type:
                    data = await response.json()
                else:
                    data = await response.text()
                if response.status != 200:
                    error_message = f"API call failed with status {response.status}"
                    if data:
                        error_message += f": {data}"
                    return {"status": response.status, "error": error_message}
                return {"status": response.status, "data": data}

    except ClientConnectorError as e:
        return {"status": 500, "error": f"Failed to connect to {url}"}

    except Exception as e:
        return {"status": 500, "error": f"Failed to make the API call"}
