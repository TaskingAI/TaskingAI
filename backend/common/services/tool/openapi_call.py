import os
from typing import Dict, Tuple, Optional
from common.models import Authentication, AuthenticationType
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


def _prepare_request_parameters(
    openapi_schema: Dict, method: str, path: str, parameter_dict: Dict
) -> Tuple[str, Optional[Dict], Optional[Dict], Optional[str]]:
    """
    Prepares request parameters for an API call based on OpenAPI schema definitions.

    :param openapi_schema: The OpenAPI specification as a dictionary.
    :param method: The HTTP method (e.g., 'GET', 'POST').
    :param path: The API endpoint path.
    :param parameter_dict: Dictionary containing parameters to be used in the request.
    :return: A tuple with the final URL, query parameters, body, and content type.
    :raises ValueError: If the path or method is not found in the OpenAPI schema.
    """

    # Extract base URL from OpenAPI schema and construct final endpoint URL
    base_url = openapi_schema["servers"][0]["url"]
    final_url = f"{base_url}{path}"
    query_params = {}
    body = None
    content_type = None

    # Verify if the provided path exists in the OpenAPI schema
    path_item = openapi_schema["paths"].get(path)
    if path_item is None:
        raise ValueError(f"No path item found for path: {path}")

    # Verify if the provided method is defined for the path in the OpenAPI schema
    operation = path_item.get(method.lower())
    if operation is None:
        raise ValueError(f"No operation found for method: {method} at path: {path}")

    # Populate query parameters and path parameters from parameter_dict
    if "parameters" in operation:
        for param in operation["parameters"]:
            param_name = param["name"]
            param_in = param["in"]
            # Set parameter value in appropriate location based on its 'in' field

            # Check for the presence of 'enum' in the parameter schema and if it contains exactly one value
            param_value = None
            if "enum" in param["schema"] and len(param["schema"]["enum"]) == 1:
                param_value = param["schema"]["enum"][0]
            elif param_name in parameter_dict:
                param_value = parameter_dict[param_name]

            if param_value is not None:
                if param_in == "query":
                    query_params[param_name] = param_value
                elif param_in == "path":
                    # Replace path parameters with corresponding values
                    final_url = final_url.replace(f"{{{param_name}}}", urllib.parse.quote(str(param_value)))

    # Append query string to the final URL if there are query parameters
    if query_params:
        final_url += "?" + urllib.parse.urlencode(query_params)

    # Handle requestBody if it's required by the operation
    if "requestBody" in operation:
        content_type, body_schema = next(iter(operation["requestBody"]["content"].items()))
        required_body_fields = list(body_schema.get("schema", {}).get("properties", {}).keys())
        properties = body_schema.get("schema", {}).get("properties", {})

        # Initialize body with default enum values if any
        body_defaults = {
            k: param["enum"][0] for k, param in properties.items() if "enum" in param and len(param["enum"]) == 1
        }
        # Update the body with parameters from parameter_dict if they are in the schema
        body = {k: parameter_dict.get(k, body_defaults.get(k)) for k in required_body_fields}

        if "application/json" in operation["requestBody"]["content"]:
            content_type = "application/json"
            body = {k: v for k, v in parameter_dict.items() if k in required_body_fields}

        elif "application/x-www-form-urlencoded" in operation["requestBody"]["content"]:
            content_type = "application/x-www-form-urlencoded"
            body = {k: v for k, v in parameter_dict.items() if k in required_body_fields}

    return final_url, query_params, body, content_type


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
    path, method_info = next(iter(openapi_schema["paths"].items()))
    method = next(iter(method_info.keys()))

    # Prepare request parameters
    url, query_params, body, content_type = _prepare_request_parameters(
        openapi_schema=openapi_schema, method=method, path=path, parameter_dict=parameters
    )

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

            if content_type == "application/json":
                request_kwargs["json"] = body
            elif content_type == "application/x-www-form-urlencoded":
                request_kwargs["data"] = body

            async with session.request(method, url, **request_kwargs) as response:
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
