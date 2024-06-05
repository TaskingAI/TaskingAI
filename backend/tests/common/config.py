import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()


class Config:

    # host
    HOST = "http://127.0.0.1"

    # service port
    WEB_SERVICE_PORT = 8080
    API_SERVICE_PORT = 8090

    # route prefix
    WEB_ROUTE_PREFIX = "/api/v1"
    API_ROUTE_PREFIX = "/v1"

    # base url
    WEB_BASE_URL = f"{HOST}:{WEB_SERVICE_PORT}{WEB_ROUTE_PREFIX}"
    API_BASE_URL = f"{HOST}:{API_SERVICE_PORT}{API_ROUTE_PREFIX}"
    OAPI_BASE_URL = API_BASE_URL


    # http proxy
    HTTP_PROXY_URL = "http://127.0.0.1:7890"

    # secret
    DEFAULT_ADMIN_USERNAME = "admin"
    DEFAULT_ADMIN_PASSWORD = "TaskingAI321"
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    TOGETHERAI_API_KEY = os.environ.get("TOGETHERAI_API_KEY")
    COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
    OPEN_WEATHER_API_KEY = os.environ.get("OPEN_WEATHER_API_KEY")
    EXCHANGERATE_API_API_KEY = os.environ.get("EXCHANGERATE_API_API_KEY")

    TEXT_EMBEDDING_MODEL = {
        "host_type": "provider",
        "name": "My Text Embedding Model",
        "model_schema_id": "openai/text-embedding-ada-002",
        "credentials": {"OPENAI_API_KEY": OPENAI_API_KEY},
    }
    CHAT_COMPLETION_MODEL = {
        "host_type": "provider",
        "name": "My Chat Completion Model",
        "model_schema_id": "openai/gpt-4",
        "credentials": {"OPENAI_API_KEY": OPENAI_API_KEY},
    }
    TOGETHERAI_TEXT_EMBEDDING_MODEL = {
        "host_type": "provider",
        "name": "Togetherai Text Embedding Model",
        "model_schema_id": "togetherai/wildcard",
        "provider_model_id": "togethercomputer/m2-bert-80M-8k-retrieval",
        "type": "text_embedding",
        "credentials": {
            "TOGETHERAI_API_KEY": TOGETHERAI_API_KEY,
        },
        "properties": {"embedding_size": 768, "input_token_limit": 8192, "max_batch_size": 2048},
    }
    TOGETHERAI_CHAT_COMPLETION_MODEL = {
        "host_type": "provider",
        "name": "Togetherai Chat Completion Model",
        "model_schema_id": "togetherai/wildcard",
        "provider_model_id": "mistralai/Mistral-7B-Instruct-v0.1",
        "type": "chat_completion",
        "credentials": {
            "TOGETHERAI_API_KEY": TOGETHERAI_API_KEY,
        },
        "properties": {
            "vision": False,
            "streaming": True,
            "function_call": True,
            "input_token_limit": 2000,
            "output_token_limit": 2000,
        },
    }
    NOT_STREAM_WILDCARD_CHAT_COMPLETION_MODEL = {
        "host_type": "provider",
        "name": "Not Stream Wildcard Chat Completion Model",
        "model_schema_id": "togetherai/wildcard",
        "provider_model_id": "mistralai/Mistral-7B-Instruct-v0.1",
        "type": "chat_completion",
        "credentials": {
            "TOGETHERAI_API_KEY": TOGETHERAI_API_KEY,
        },
        "properties": {
            "vision": False,
            "streaming": False,
            "function_call": False,
            "input_token_limit": 2000,
            "output_token_limit": 2000,
        },
    }
    DEBUG_TEXT_EMBEDDING_MODEL = {
        "host_type": "provider",
        "model_schema_id": "debug/debug-text-embedding-256",
        "name": "debug-text-embedding256",
        "credentials": {"DEBUG_API_KEY": "12345678"},
    }
    WILDCARD_TEXT_EMBEDDING_MODEL = {
        "host_type": "provider",
        "name": "Wildcard Text Embedding Model",
        "model_schema_id": "debug/debug-wildcard",
        "provider_model_id": "debug-wildcard",
        "type": "text_embedding",
        "credentials": {"DEBUG_API_KEY": "12345678"},
        "properties": {"embedding_size": 512, "input_token_limit": 8192, "max_batch_size": 2048},
    }
    WILDCARD_CHAT_COMPLETION_MODEL = {
        "host_type": "provider",
        "name": "Wildcard Chat Completion Model",
        "model_schema_id": "debug/debug-wildcard",
        "provider_model_id": "debug-wildcard",
        "type": "chat_completion",
        "credentials": {"DEBUG_API_KEY": "12345678"},
        "properties": {
            "streaming": True,
            "function_call": True,
        },
    }
    CUSTOM_HOST_TEXT_EMBEDDING_MODEL = {
        "host_type": "provider",
        "name": "Custom_host Text Embedding Model",
        "model_schema_id": "custom_host/openai-text-embedding",
        "credentials": {
            "CUSTOM_HOST_API_KEY": OPENAI_API_KEY,
            "CUSTOM_HOST_ENDPOINT_URL": "https://api.openai.com/v1/embeddings",
            "CUSTOM_HOST_MODEL_ID": "text-embedding-ada-002",
        },
        "properties": {"embedding_size": 1536, "input_token_limit": 8192, "max_batch_size": 2048},
    }
    CUSTOM_HOST_CHAT_COMPLETION_MODEL = {
        "host_type": "provider",
        "name": "Custom_host Chat Completion Model",
        "model_schema_id": "custom_host/openai-function-call",
        "credentials": {
            "CUSTOM_HOST_API_KEY": OPENAI_API_KEY,
            "CUSTOM_HOST_ENDPOINT_URL": "https://api.openai.com/v1/chat/completions",
            "CUSTOM_HOST_MODEL_ID": "gpt-3.5-turbo",
        },
        "properties": {
            "streaming": True,
            "function_call": True,
        },
    }
    RERANK_MODEL = {
            "host_type": "provider",
            "model_schema_id": "cohere/rerank-english-v2.0",
            "name": "Rerank Model",
            "credentials": {"COHERE_API_KEY": COHERE_API_KEY},
        }

    DEBUG_ERROR_MODEL = {
            "host_type": "provider",
            "name": "Debug Error Model",
            "model_schema_id": "debug/debug-error",
            "credentials": {"DEBUG_API_KEY": "12345678"},
        }

    def __init__(self):

        self.TEST_MODE = os.environ.get("TEST_MODE")

        if self.TEST_MODE == "TASKINGAI_WEB_TEST":
            self.BASE_URL = self.WEB_BASE_URL
            self.rerank_model_id = None
        if self.TEST_MODE == "TASKINGAI_API_TEST":
            login_url = f"{self.WEB_BASE_URL}/admins/login"
            login_data = {"username": self.DEFAULT_ADMIN_USERNAME, "password": self.DEFAULT_ADMIN_PASSWORD}
            token = self.get_token(login_url, login_data)
            model_url = f"{self.WEB_BASE_URL}/models"
            self.text_embedding_model_id = self.get_model(model_url, self.TEXT_EMBEDDING_MODEL, token)
            self.chat_completion_model_id = self.get_model(model_url, self.CHAT_COMPLETION_MODEL, token)
            self.togetherai_text_embedding_model_id = self.get_model(
                model_url, self.TOGETHERAI_TEXT_EMBEDDING_MODEL, token
            )
            time.sleep(1)
            self.togetherai_chat_completion_model_id = self.get_model(
                model_url, self.TOGETHERAI_CHAT_COMPLETION_MODEL, token
            )
            time.sleep(1)
            self.not_stream_wildcard_chat_completion_model_id = self.get_model(
                model_url, self.NOT_STREAM_WILDCARD_CHAT_COMPLETION_MODEL, token
            )
            self.debug_text_embedding_model_id = self.get_model(model_url, self.DEBUG_TEXT_EMBEDDING_MODEL, token)

            self.custom_host_text_embedding_model_id = self.get_model(
                model_url, self.CUSTOM_HOST_TEXT_EMBEDDING_MODEL, token
            )
            self.custom_host_chat_completion_model_id = self.get_model(
                model_url, self.CUSTOM_HOST_CHAT_COMPLETION_MODEL, token
            )
            self.rerank_model_id = self.get_model(model_url, self.RERANK_MODEL, token)
            self.debug_error_model_id = self.get_model(model_url, self.DEBUG_ERROR_MODEL, token)
            self.TEXT_EMBEDDING_MODEL["fallbacks"] = {
                "model_list": [{"model_id": self.togetherai_text_embedding_model_id}]}
            self.fallbacks_text_embedding_model_id = self.get_model(model_url, self.TEXT_EMBEDDING_MODEL, token)
            self.CHAT_COMPLETION_MODEL["fallbacks"] = {
                "model_list": [{"model_id": self.custom_host_chat_completion_model_id}]}
            self.fallbacks_chat_completion_model_id = self.get_model(model_url, self.CHAT_COMPLETION_MODEL, token)
            self.RERANK_MODEL["fallbacks"] = {"model_list": [{"model_id": self.rerank_model_id}]}
            self.fallbacks_rerank_model_id = self.get_model(model_url, self.RERANK_MODEL, token)
            self.DEBUG_ERROR_MODEL["fallbacks"] = {"model_list": [{"model_id": self.chat_completion_model_id}]}
            self.fallbacks_debug_error_model_id = self.get_model(model_url, self.DEBUG_ERROR_MODEL, token)
            apikey_url = f"{self.WEB_BASE_URL}/apikeys"
            create_apikey_dict = {"name": "test_apikey"}
            self.Authentication = self.get_apikey(apikey_url, create_apikey_dict, token)
            bundle_instance_dict = {
                "name": "hello",
                "credentials": {"OPEN_WEATHER_API_KEY": self.OPEN_WEATHER_API_KEY},
                "bundle_id": "open_weather",
            }
            bundle_instance_url = f"{self.WEB_BASE_URL}/bundle_instances"
            self.create_bundle_instance(bundle_instance_url, bundle_instance_dict, token)
            self.BASE_URL = self.API_BASE_URL

    def get_token(self, url, data):
        response = requests.post(url, json=data)
        res_data = response.json()["data"]
        return res_data["token"]

    def get_model(self, model_url, model_data, token):

        from backend.tests.common.utils import get_headers

        response = requests.post(model_url, headers=get_headers(token), json=model_data)
        model_id = response.json()["data"]["model_id"]
        return model_id

    def get_apikey(self, apikey_url, apikey_data, token):
        from backend.tests.common.utils import get_headers

        apikeys = requests.get(apikey_url, headers=get_headers(token))
        apikeys_data = apikeys.json()["data"]
        if len(apikeys_data) > 0:
            apikey_id = apikeys_data[0]["apikey_id"]
            apikey_res = requests.get(f"{apikey_url}/{apikey_id}", headers=get_headers(token), params={"plain": True})
            return apikey_res.json()["data"]["apikey"]
        else:
            create_apikey_res = requests.post(apikey_url, headers=get_headers(token), json=apikey_data)
            apikey_id = create_apikey_res.json()["data"]["apikey_id"]
            apikey_res = requests.get(f"{apikey_url}/{apikey_id}", headers=get_headers(token), params={"plain": True})
            return apikey_res.json()["data"]["apikey"]

    def create_bundle_instance(self, bundle_instance_url, bundle_instance_dict, token):
        from backend.tests.common.utils import get_headers

        res = requests.post(bundle_instance_url, json=bundle_instance_dict, headers=get_headers(token))

CONFIG = Config()
