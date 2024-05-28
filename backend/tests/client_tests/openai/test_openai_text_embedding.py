from backend.tests.client_tests.openai import client, OPENAI_TEXT_EMBEDDING_MODEL_ID
import pytest


@pytest.mark.api_test
class TestOpenAITextEmbedding:

    input_list = [{"input": "hello, nice to meet you"}, {"input": ["hello, nice to meet you", "i'm fine thank you"]}]

    long_list_text = {"input": ["*" * 600, "!" * 600]}
    empty_list_text = {"input": []}

    error_input_list = [
        {"input": 100},
        {"input": ["hello, nice to meet you", 100]},
    ]

    @pytest.mark.run(order=121)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("input_data", input_list)
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai__001-002")
    async def test_text_embedding(self, input_data):

        res = client.embeddings.create(model=OPENAI_TEXT_EMBEDDING_MODEL_ID, input=input_data)
        for item in res.data:
            assert all(isinstance(value, float) for value in item.embedding)

    @pytest.mark.run(order=121)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_004")
    async def test_text_embedding_with_long_list_text(self):

        res = client.embeddings.create(model=OPENAI_TEXT_EMBEDDING_MODEL_ID, input=self.long_list_text)
        for item in res.data:
            assert all(isinstance(value, float) for value in item.embedding)

    @pytest.mark.run(order=121)
    @pytest.mark.asyncio
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_004")
    async def test_text_embedding_with_empty_list_text(self):
        res = client.embeddings.create(model=OPENAI_TEXT_EMBEDDING_MODEL_ID, input=self.empty_list_text)
        for item in res.data:
            assert all(isinstance(value, float) for value in item.embedding)

    @pytest.mark.run(order=121)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("input_data", error_input_list)
    @pytest.mark.version("0.3.1")
    @pytest.mark.test_id("openai_003")
    async def test_error_text_embedding(self, input_data):
        with pytest.raises(Exception) as e:
            client.embeddings.create(model=OPENAI_TEXT_EMBEDDING_MODEL_ID, input=self.error_input_list)
        assert e.value.code == "REQUEST_VALIDATION_ERROR"
