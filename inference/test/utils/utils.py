import yaml
import os
import aiohttp
import json
from dotenv import load_dotenv
from app.models import provider_credentials
from config import CONFIG
import copy
import math

white_list_providers = [
    "azure_openai",
    "zhipu",
    "baichuan",
    "hugging_face",
    "tongyi",
    "wenxin",
    "moonshot",
    "aws_bedrock",
    "yi",
    "minimax",
    "sensetime",
    "leptonai",
    "volcengine",
    "togetherai",
]
white_list_models = [
    "google_gemini/gemini-1.0-pro-vision",
    "google_gemini/gemini-1.5-pro",
    "togetherai/meta-llama/Llama-2-70b-chat-hf",
    "mistralai/mistral-small-latest",
]

load_dotenv()

functions = [
    {
        "name": "make_scatter_plot",
        "description": "Generate a scatter plot from the given data",
        "parameters": {
            "type": "object",
            "properties": {
                "x_values": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "The x-axis values for the data points",
                },
                "y_values": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "The y-axis values for the data points",
                },
            },
            "required": ["x_values", "y_values"],
        },
    }
]

function_message = [
    {
        "content": "",
        "role": "assistant",
        "function_calls": [
            {
                "id": "P3lfrirIfyIJe8rHvAom2kkF",
                "name": "make_scatter_plot",
                "arguments": {"x_values": [1, 2], "y_values": [3, 4]},
            }
        ],
    },
    {"content": "*  *", "id": "P3lfrirIfyIJe8rHvAom2kkF", "role": "function"},
]

default_config_values = {
    "temperature": 0.5,
    "top_p": 0.5,
    "max_tokens": 3,
}


# Read all YAML files in the specified directory
def get_yaml_files(directory):
    yaml_files = [f for f in os.listdir(directory) if f.endswith(".yml") or f.endswith(".yaml")]
    return yaml_files


# Read a single YAML file
def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def generate_test_cases(model_type):
    if model_type not in ["chat_completion", "text_embedding", "rerank"]:
        raise ValueError("'type' must be 'chat_completion' or 'text_embedding' or 'rerank'")

    providers_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../providers")
    provider_ids = [name for name in os.listdir(providers_path) if os.path.isdir(os.path.join(providers_path, name))]
    provider_ids = [name for name in provider_ids if not name.startswith("_") and not name.startswith("template")]

    cases = []
    tested_providers = set()  # Keep track of providers that have been tested.
    for provider_id in provider_ids:
        if provider_id in white_list_providers:
            continue
        if provider_id == "debug" and CONFIG.PROD:
            continue
        print("Adding test cases for provider: ", provider_id)
        models_path = os.path.join(providers_path, provider_id, "resources/models")
        yaml_files = get_yaml_files(models_path)

        for yaml_file in yaml_files:
            tested_providers.add(provider_id)

            file_path = os.path.join(models_path, yaml_file)
            yaml_data = load_yaml(file_path)
            if (
                yaml_data.get("type") != model_type
                or yaml_data["model_schema_id"] in white_list_models
                or yaml_file == "wildcard.yml"
                or not yaml_data.get("provider_model_id")
            ):
                continue

            properties = yaml_data.get("properties", {})
            config_schemas = yaml_data.get("config_schemas") or []
            allowed_configs = [config["config_id"] for config in config_schemas]
            base_test_case = {"model_schema_id": yaml_data["model_schema_id"], "allowed_configs": allowed_configs}

            if model_type == "chat_completion":
                function_call = properties.get("function_call", False)
                streaming = properties.get("streaming", False)
                vision = properties.get("vision", False)
                chat_completion_case = {
                    **base_test_case,
                    "function_call": function_call,
                    "message": [
                        {
                            "role": "user",
                            "content": "Draw a scatter plot with x values 1, 2 and y values 3, 4",
                        },
                    ],
                }
                if function_call:
                    chat_completion_case["functions"] = functions
                    if streaming:
                        cases.append({**chat_completion_case, "stream": True, "vision": vision})
                    # Always generate test cases with streaming set to false
                    cases.append({**chat_completion_case, "stream": False, "vision": vision})
                    new_chat_completion_case = copy.deepcopy(chat_completion_case)
                    new_chat_completion_case["message"].extend(function_message)
                    new_chat_completion_case["function_call"] = False
                    if streaming:
                        cases.append({**new_chat_completion_case, "stream": True, "vision": vision})
                    cases.append({**new_chat_completion_case, "stream": False, "vision": vision})
                else:
                    if streaming:
                        cases.append({**chat_completion_case, "stream": True, "vision": vision})
                    cases.append({**chat_completion_case, "stream": False, "vision": vision})
            elif model_type == "text_embedding":
                embedding_size = properties.get("embedding_size", 0)
                text_embedding_case = {**base_test_case, "embedding_size": embedding_size}
                cases.append(text_embedding_case)
            elif model_type == "rerank":
                rerank_case = {**base_test_case}
                cases.append(rerank_case)

    return cases


def generate_wildcard_test_cases(model_type: str):
    final_test_cases = []
    allowed_configs = ["temperature", "top_p", "max_tokens", "top_k", "stop"]

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wildcard_test_cases.yml")
    yaml_data = load_yaml(file_path)
    wildcard_test_cases = yaml_data.get("wildcard_test_cases", [])

    for provider in wildcard_test_cases:
        cases = provider.get("cases", [])

        for case in cases:
            if case.get("model_type") == model_type:
                base_test_case = {
                    "model_schema_id": case["model_schema_id"],
                    "provider_model_id": case["provider_model_id"],
                    "message": case.get("message", []),
                }
                if model_type == "chat_completion":
                    base_test_case["allowed_configs"] = allowed_configs
                    function_call = case.get("function_call", False)
                    streaming = case.get("streaming", False)

                    chat_completion_case = {
                        **base_test_case,
                        "function_call": function_call,
                        "message": [
                            {
                                "role": "user",
                                "content": "Draw a scatter plot with x values 1, 2 and y values 3, 4",
                            },
                        ],
                    }
                    if function_call:
                        chat_completion_case["functions"] = functions
                        if streaming:
                            final_test_cases.append({**chat_completion_case, "stream": True})
                        # Always generate test cases with streaming set to false
                        final_test_cases.append({**chat_completion_case, "stream": False})
                        new_chat_completion_case = copy.deepcopy(chat_completion_case)
                        new_chat_completion_case["message"].extend(function_message)
                        new_chat_completion_case["function_call"] = False
                        if streaming:
                            final_test_cases.append({**new_chat_completion_case, "stream": True})
                        final_test_cases.append({**new_chat_completion_case, "stream": False})
                    else:
                        if streaming:
                            final_test_cases.append({**chat_completion_case, "stream": True})
                        final_test_cases.append({**chat_completion_case, "stream": False})
                elif model_type == "text_embedding":
                    properties = case.get("properties", {})
                    embedding_size = properties.get("embedding_size", 0)
                    test_case = {**base_test_case, "embedding_size": embedding_size}
                    final_test_cases.append(test_case)
                elif model_type == "rerank":
                    final_test_cases.append(base_test_case)

    return final_test_cases


def generate_test_cases_for_validation():
    providers_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../providers")
    provider_ids = [name for name in os.listdir(providers_path) if os.path.isdir(os.path.join(providers_path, name))]
    provider_ids = [name for name in provider_ids if not name.startswith("_") and not name.startswith("template")]

    cases = []
    for provider_id in provider_ids:
        if provider_id in white_list_providers:
            continue
        if provider_id == "debug" and CONFIG.PROD:
            continue
        print("Adding test cases for provider: ", provider_id)
        provider_path = os.path.join(providers_path, provider_id, "resources")
        models_path = os.path.join(providers_path, provider_id, "resources/models")
        yaml_files = get_yaml_files(models_path)

        yaml_data = None
        for yaml_file in yaml_files:
            file_path = os.path.join(models_path, yaml_file)
            yaml_data = load_yaml(file_path)
            if yaml_data["model_schema_id"] not in white_list_models and yaml_file != "wildcard.yml":
                break
        if not yaml_data or yaml_data["type"] == "wildcard":
            continue
        provider_yaml_data = load_yaml(os.path.join(provider_path, "provider.yml"))

        credentials_schema = provider_yaml_data["credentials_schema"]

        credentials = {
            key: provider_credentials.aes_encrypt(os.environ.get(key)) for key in credentials_schema["required"]
        }
        base_test_case = {
            "model_schema_id": yaml_data["model_schema_id"],
            "model_type": yaml_data["type"],
            "credentials": credentials,
        }
        cases.append(base_test_case)

    return cases


def generate_wildcard_test_case_for_validation():
    # load wildcard_test_cases.yml
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wildcard_test_cases.yml")
    yaml_data = load_yaml(file_path)

    # get wildcard_test_cases
    wildcard_validation_test_cases = yaml_data.get("wildcard_test_cases", [])
    providers_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../providers")

    cases = []

    for provider in wildcard_validation_test_cases:
        provider_id = provider["provider_id"]
        for test_case in provider.get("cases", []):
            provider_path = os.path.join(providers_path, provider_id, "resources")
            provider_yaml_data = load_yaml(os.path.join(provider_path, "provider.yml"))
            credentials_schema = provider_yaml_data["credentials_schema"]
            credentials = {
                key: provider_credentials.aes_encrypt(os.environ.get(key)) for key in credentials_schema["required"]
            }

            model_type = test_case.get("model_type")

            if model_type == "chat_completion":
                cases.append({**test_case, "credentials": credentials})
            elif model_type == "text_embedding":
                properties = test_case.get("properties", {})
                if "embedding_size" not in properties:
                    raise ValueError("Embedding size is required for text_embedding models.")
                cases.append({**test_case, "credentials": credentials, "properties": properties})

    return cases


SSE_DONE_MSG = "data: [DONE]\n\n"


async def sse_stream(
    url: str,
    payload: dict,
):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            buffer = ""
            # handle streaming response in different json chunks
            async for line in response.content:
                if line.endswith(b"\n"):
                    buffer += line.decode()
                    if buffer.endswith("\n\n"):
                        lines = buffer.strip().split("\n")
                        event_data = lines[0][len("data: ") :]
                        if event_data != "[DONE]":
                            try:
                                data = json.loads(event_data)
                                yield data
                            except json.decoder.JSONDecodeError:
                                continue
                        buffer = ""


class ResponseWrapper:
    def __init__(self, status: int, json_data: dict):
        self.status_code = status
        self._json_data = json_data

    def json(self):
        return self._json_data


def check_order(lst, key):
    return all(lst[i][key] >= lst[i + 1][key] for i in range(len(lst) - 1))


def is_unit_vector(vector, tolerance=1e-3):
    norm = math.sqrt(sum(x**2 for x in vector))
    return abs(norm - 1.0) <= tolerance


def is_provider_service_error(response: ResponseWrapper) -> bool:
    return (
        response.status_code == 400
        and response.json().get("error").get("message") == "Provider's service is unavailable"
    )
