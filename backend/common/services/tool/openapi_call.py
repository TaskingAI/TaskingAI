import os
from typing import Dict
from common.models import Authentication, AuthenticationType
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
import logging

logger = logging.getLogger(__name__)


def _prepare_headers(authentication: Authentication, extra_headers: Dict) -> Dict:
    headers = {}

    if extra_headers:
        headers.update(extra_headers)

    if authentication:
        if authentication.type == AuthenticationType.basic:
            # Basic Authentication: Encode the secret and add it to headers
            headers["Authorization"] = f"Basic {authentication.secret}"

        elif authentication.type == AuthenticationType.bearer:
            # Bearer Authentication: Add the secret as a bearer token
            headers["Authorization"] = f"Bearer {authentication.secret}"

        elif authentication.type == AuthenticationType.custom:
            # Custom Authentication: Return the custom content as headers
            headers.update(authentication.content)

    return headers


def _prepare_request_parameters(openapi_path_schema, parameters):
    """Prepare URL path, query parameters and request body according to OpenAPI schema."""
    path_params, query_params, body, content_type = {}, {}, None, None

    for param in openapi_path_schema.get("parameters", []):
        param_name = param["name"]
        param_in = param["in"]
        param_value = None

        # Check if the parameter has an enum with only one value
        if "enum" in param["schema"] and len(param["schema"]["enum"]) == 1:
            # Use the single enum value
            param_value = param["schema"]["enum"][0]
        elif parameters:
            param_value = parameters.get(param_name)

        if param_value is not None:
            if param_in == "path":
                path_params[param_name] = param_value
            elif param_in == "query":
                query_params[param_name] = param_value

    # handle request body
    if "requestBody" in openapi_path_schema:
        content_type = openapi_path_schema["requestBody"]["content"]
        if parameters:
            if "application/json" in content_type:
                body = parameters
            elif "application/x-www-form-urlencoded" in content_type:
                body = parameters

    return path_params, query_params, body, content_type


class ActionApiCallException(Exception):
    pass


async def call_action_api(
    openapi_schema: Dict, authentication: Authentication, parameters: Dict, headers: Dict
) -> Dict:
    """
    Call an API according to OpenAPI schema.
    :param openapi_schema: the OpenAPI schema of the action
    :param authentication: the authentication of the action
    :param parameters: the parameters of the API call
    :param headers: the extra headers of the API call
    :return:
    """

    # Extract information from OpenAPI schema
    base_url = openapi_schema["servers"][0]["url"]
    path, method_info = next(iter(openapi_schema["paths"].items()))
    method = next(iter(method_info.keys()))

    # Prepare request parameters
    openapi_path_schema = openapi_schema.get("paths", {}).get(path, {}).get(method, {})
    if not openapi_path_schema:
        raise ActionApiCallException(f"Path {path} with method {method} is not found in OpenAPI schema")

    path_params, query_params, body, content_type = _prepare_request_parameters(openapi_path_schema, parameters)

    # Substitute path parameters in URL
    for key, value in path_params.items():
        path = path.replace(f"{{{key}}}", str(value))

    url = f"{base_url}{path}"
    headers = _prepare_headers(authentication, headers)

    # Debug
    logger.debug(
        f"Calling {method} {url} Headers: {headers} "
        f"Query parameters: {query_params} Body: {body} Content-Type: {content_type}"
    )

    # Making the API call
    try:
        async with aiohttp.ClientSession() as session:
            request_kwargs = {"params": query_params, "headers": headers}

            if os.environ.get("HTTP_PROXY_URL"):
                request_kwargs["proxy"] = os.environ.get("HTTP_PROXY_URL")

            if content_type:
                if "application/json" in content_type.keys():
                    request_kwargs["json"] = body
                elif "application/x-www-form-urlencoded" in content_type.keys():
                    request_kwargs["data"] = body

            async with session.request(method, url, **request_kwargs) as response:
                content_type = response.headers.get("Content-Type", "").lower()
                if "application/json" in content_type:
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
