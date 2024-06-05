import pytest
import json
import asyncio
from backend.tests.api_services.model.model import create_model, list_models, get_model, update_model, delete_model
from backend.tests.common.config import CONFIG
from backend.tests.common.utils import assume_model


@pytest.mark.web_test
class TestModel:

    model_id = "TpUiB8O4"

    create_model_list = [
        {
            "host_type": "provider",
            "name": "Openai Text Embedding Model",
            "model_schema_id": "openai/text-embedding-ada-002",
            "credentials": {"OPENAI_API_KEY": CONFIG.OPENAI_API_KEY},
        },
        {
            "host_type": "provider",
            "name": "Openai Chat Completion Model",
            "model_schema_id": "openai/gpt-3.5-turbo",
            "credentials": {"OPENAI_API_KEY": CONFIG.OPENAI_API_KEY},
            "configs": {
                "temperature": 1.0,
                "max_tokens": 4096,
                "top_p": 1.0,
                "stop": ["test1", "test2", "test3"],
                "test": "test",
            },
        },
        {
            "host_type": "provider",
            "model_schema_id": "cohere/rerank-english-v2.0",
            "name": "Rerank Model",
            "credentials": {"COHERE_API_KEY": CONFIG.COHERE_API_KEY},
        },
    {
            "host_type": "provider",
            "name": "Debug Error Model",
            "model_schema_id": "debug/debug-error",
            "credentials": {"DEBUG_API_KEY": "12345678"},
        },
        {
            "host_type": "provider",
            "name": "Togetherai Text Embedding Model",
            "model_schema_id": "togetherai/wildcard",
            "provider_model_id": "togethercomputer/m2-bert-80M-8k-retrieval",
            "type": "text_embedding",
            "credentials": {
                "TOGETHERAI_API_KEY": CONFIG.TOGETHERAI_API_KEY,
            },
            "properties": {"embedding_size": 768, "input_token_limit": 8192, "max_batch_size": 2048},
        },
        {
            "host_type": "provider",
            "name": "Togetherai Chat Completion Model",
            "model_schema_id": "togetherai/wildcard",
            "provider_model_id": "mistralai/Mistral-7B-Instruct-v0.1",
            "type": "chat_completion",
            "credentials": {
                "TOGETHERAI_API_KEY": CONFIG.TOGETHERAI_API_KEY,
            },
            "properties": {
                "vision": False,
                "streaming": True,
                "function_call": True,
                "input_token_limit": 2000,
                "output_token_limit": 2000,
            },
            "configs": {"temperature": 0.0, "max_tokens": 4096, "top_p": 0.0, "stop": [], "test": "test"},
        },
        {
            "host_type": "provider",
            "name": "Not Stream Wildcard Chat Completion Model",
            "model_schema_id": "togetherai/wildcard",
            "provider_model_id": "mistralai/Mistral-7B-Instruct-v0.1",
            "type": "chat_completion",
            "credentials": {
                "TOGETHERAI_API_KEY": CONFIG.TOGETHERAI_API_KEY,
            },
            "properties": {
                "vision": False,
                "streaming": False,
                "function_call": False,
                "input_token_limit": 2000,
                "output_token_limit": 2000,
            },
            "configs": {"temperature": 0.0, "max_tokens": 1, "top_p": 0.0, "stop": [], "test": "test"},
        },
        {
            "host_type": "provider",
            "name": "Custom_host Text Embedding Model",
            "model_schema_id": "custom_host/openai-text-embedding",
            "credentials": {
                "CUSTOM_HOST_API_KEY": CONFIG.OPENAI_API_KEY,
                "CUSTOM_HOST_ENDPOINT_URL": "https://api.openai.com/v1/embeddings",
                "CUSTOM_HOST_MODEL_ID": "text-embedding-ada-002",
            },
            "properties": {"embedding_size": 1536, "input_token_limit": 8192, "max_batch_size": 2048},
        },
        {
            "host_type": "provider",
            "name": "Custom_host Chat Completion Model",
            "model_schema_id": "custom_host/openai-function-call",
            "credentials": {
                "CUSTOM_HOST_API_KEY": CONFIG.OPENAI_API_KEY,
                "CUSTOM_HOST_ENDPOINT_URL": "https://api.openai.com/v1/chat/completions",
                "CUSTOM_HOST_MODEL_ID": "gpt-3.5-turbo",
            },
            "properties": {
                "streaming": True,
                "function_call": True,
            },
            "configs": {
                "temperature": 0.5,
                "max_tokens": 4096,
                "top_p": 0.5,
                "stop": [],
            },
        },
    ]

    update_model_list = [
        {
            "host_type": "provider",
            "name": "My Chat Completion Model Test",
        },
        {"host_type": "provider", "credentials": {"OPENAI_API_KEY": CONFIG.OPENAI_API_KEY}},
        {
            "host_type": "provider",
            "model_schema_id": "openai/gpt-4",
            "provider_model_id": "gpt-4",
            "type": "chat_completion",
            "properties": {
                "function_call": True,
                "streaming": True,
                "vision": False,
                "input_token_limit": 8192,
                "output_token_limit": 4096,
            },
        },
        {
            "host_type": "provider",
            "configs": {
                "temperature": 1.0,
                "max_tokens": 4096,
                "top_p": 1.0,
                "stop": ["test1", "test2", "test3"],
                "test": "test",
            },
        },
    ]

    @pytest.mark.run(order=112)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("create_model_data", create_model_list)
    async def test_create_model(self, create_model_data):

        create_model_data.pop("host_type", None)

        res = await create_model(create_model_data)
        res_json = res.json()

        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("name") == create_model_data["name"]
        assert res_json.get("data").get("model_schema_id") == create_model_data["model_schema_id"]

        assume_model(res, create_model_data)
        TestModel.model_id = res_json.get("data").get("model_id")
        if create_model_data.get("name") == "Openai Text Embedding Model":
            CONFIG.text_embedding_model_id = TestModel.model_id
        if create_model_data.get("name") == "Openai Chat Completion Model":
            CONFIG.chat_completion_model_id = TestModel.model_id
        if create_model_data.get("name") == "Togetherai Text Embedding Model":
            CONFIG.togetherai_text_embedding_model_id = TestModel.model_id
        if create_model_data.get("name") == "Togetherai Chat Completion Model":
            CONFIG.togetherai_chat_completion_model_id = TestModel.model_id
        if create_model_data.get("name") == "Debug Error Model":
            CONFIG.debug_error_model_id = TestModel.model_id
        if create_model_data.get("name") == "Custom_host Text Embedding Model":
            CONFIG.custom_host_text_embedding_model_id = TestModel.model_id
        if create_model_data.get("name") == "Custom_host Chat Completion Model":
            CONFIG.custom_host_chat_completion_model_id = TestModel.model_id
        if create_model_data.get("name") == "Not Stream Wildcard Chat Completion Model":
            CONFIG.not_stream_wildcard_chat_completion_model_id = TestModel.model_id
        if create_model_data.get("name") == "Rerank Model":
            CONFIG.rerank_model_id = TestModel.model_id

        get_res = await get_model(TestModel.model_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 200, get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("model_id") == TestModel.model_id

        assert get_res_json.get("data").get("name") == create_model_data["name"]
        assert get_res_json.get("data").get("model_schema_id") == create_model_data["model_schema_id"]
        assume_model(get_res, create_model_data)


    @pytest.mark.asyncio
    @pytest.mark.run(order=113)
    async def test_list_models(self):

        list_model_data_list = [
            {
                "limit": 10,
                "order": "asc",
                "prefix_filter": json.dumps({"name": "Openai Text"}),
            },
            {
                "limit": 10,
                "order": "asc",
                "prefix_filter": json.dumps({"model_id": TestModel.model_id[:8]}),
            },
            {"limit": 10, "order": "desc", "equal_filter": json.dumps({"type": "chat_completion"})},
            {
                "limit": 10,
                "order": "desc",
                "after": TestModel.model_id,
            }
        ]

        for index, list_model_data in enumerate(list_model_data_list):
            if "API" in CONFIG.TEST_MODE:
                if list_model_data.get("prefix_filter") or list_model_data.get("equal_filter"):
                    continue
            res = await list_models(list_model_data)
            res_json = res.json()

            assert res.status_code == 200, res.json()
            assert res_json.get("status") == "success"
            if index <= 1:
                assert len(res_json.get("data")) == 1
                assert res_json.get("fetched_count") == 1
                if list_model_data.get("prefix_filter"):
                    prefix_filter_dict = json.loads(list_model_data.get("prefix_filter"))
                    for key in prefix_filter_dict:
                        assert res_json.get("data")[0].get(key).startswith(prefix_filter_dict.get(key))
            if index == 2:

                assert len(res_json.get("data")) == 5
                assert res_json.get("fetched_count") == 5
                for model in res_json.get("data"):
                    assert model.get("type") == "chat_completion"
            if index == 3:

                assert len(res_json.get("data")) == 8
                assert res_json.get("fetched_count") == 8

            assert res_json.get("has_more") is False

    @pytest.mark.asyncio
    @pytest.mark.run(order=114)
    @pytest.mark.parametrize("create_model_data", create_model_list[:4])
    async def test_create_model_with_fallbacks(self, create_model_data):

        if create_model_data.get("name") == "Openai Text Embedding Model":
            create_model_data.update(
                {"fallbacks": {"model_list": [{"model_id": CONFIG.togetherai_text_embedding_model_id}]}}
            )
        if create_model_data.get("name") == "Openai Chat Completion Model":
            create_model_data.update(
                {"fallbacks": {"model_list": [{"model_id": CONFIG.custom_host_chat_completion_model_id}]}}
            )
        if create_model_data.get("name") == "Rerank Model":
            create_model_data.update({"fallbacks": {"model_list": [{"model_id": CONFIG.rerank_model_id}]}})
        if create_model_data.get("name") == "Debug Error Model":
            create_model_data.update(
                {
                    "fallbacks": {
                        "model_list": [
                            {"model_id": CONFIG.chat_completion_model_id},
                        ]
                    }
                }
            )

        res = await create_model(create_model_data)
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("name") == create_model_data["name"]
        assert res_json.get("data").get("model_schema_id") == create_model_data["model_schema_id"]
        assume_model(res, create_model_data)

        model_id = res_json.get("data").get("model_id")
        if create_model_data.get("name") == "Openai Text Embedding Model":
            CONFIG.fallbacks_text_embedding_model_id = model_id
        if create_model_data.get("name") == "Openai Chat Completion Model":
            CONFIG.fallbacks_chat_completion_model_id = model_id
        if create_model_data.get("name") == "Rerank Model":
            CONFIG.fallbacks_rerank_model_id = model_id
        if create_model_data.get("name") == "Debug Error Model":
            CONFIG.fallbacks_debug_error_model_id = model_id

        get_res = await get_model(model_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 200, get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("model_id") == model_id

        assert get_res_json.get("data").get("name") == create_model_data["name"]
        assert get_res_json.get("data").get("model_schema_id") == create_model_data["model_schema_id"]
        assume_model(get_res, create_model_data)

    @pytest.mark.asyncio
    @pytest.mark.run(order=114)
    async def test_get_model(self):
        res = await get_model(TestModel.model_id)
        res_json = res.json()


        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("model_id") == TestModel.model_id


    @pytest.mark.asyncio
    @pytest.mark.run(order=115)
    @pytest.mark.parametrize("update_model_data", update_model_list)
    async def test_update_model(self, update_model_data):

        update_model_data.pop("host_type", None)

        res = await update_model(CONFIG.chat_completion_model_id, update_model_data)
        res_json = res.json()

        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("model_id") == CONFIG.chat_completion_model_id
        assume_model(res, update_model_data)

        get_res = await get_model(CONFIG.chat_completion_model_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 200, get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("model_id") == CONFIG.chat_completion_model_id
        assume_model(get_res, update_model_data)

    @pytest.mark.asyncio
    @pytest.mark.run(order=115)
    async def test_update_model_with_fallbacks(self):

        update_model_data = {
                "type": "chat_completion",
                "fallbacks": {
                    "model_list": [
                        {"model_id": CONFIG.fallbacks_chat_completion_model_id},
                    ]
                },
            }

        res = await update_model(CONFIG.chat_completion_model_id, update_model_data)
        res_json = res.json()

        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"
        assert res_json.get("data").get("model_id") == CONFIG.chat_completion_model_id
        assume_model(res, update_model_data)

        get_res = await get_model(CONFIG.chat_completion_model_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 200, get_res.json()
        assert get_res_json.get("status") == "success"
        assert get_res_json.get("data").get("model_id") == CONFIG.chat_completion_model_id
        assume_model(get_res, update_model_data)

    @pytest.mark.asyncio
    @pytest.mark.run(order=240)
    async def test_delete_model(self):

        res = await delete_model(TestModel.model_id)
        res_json = res.json()
        assert res.status_code == 200, res.json()
        assert res_json.get("status") == "success"

        get_res = await get_model(TestModel.model_id)
        get_res_json = get_res.json()
        assert get_res.status_code == 404, get_res.json()
        assert get_res_json.get("status") == "error"
        assert get_res_json.get("error").get("code") == "OBJECT_NOT_FOUND"

