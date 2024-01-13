import aiohttp
from typing import List
from common.utils import ResponseWrapper, check_http_error
from config import CONFIG
from common.models import Model
import hashlib


async def _inference(
    embedding_model: Model,
    input_text_list: List[str],
    input_type: str,
) -> ResponseWrapper:
    """
    make the text embedding inference request
    :param embedding_model: the embedding model to use
    :param input_text_list: the input text list
    :param input_type: the input type
    :return: the inference response
    """

    model_schema = embedding_model.model_schema()

    payload = {
        "provider_model_id": model_schema.provider_model_id,
        "provider_id": model_schema.provider_id,
        "credentials": embedding_model.encrypted_credentials,
        # todo encrypted_credentials
        "input": input_text_list,
        "input_type": input_type,
    }

    async with aiohttp.ClientSession() as session:
        url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/inference/text_embedding"
        response = await session.post(url, json=payload)
        return ResponseWrapper(response.status, await response.json())


def _generate_random_unit_vector(text, dim):
    """
    generate a random unit vector for development purpose
    :param text: the input text
    :param dim: the dimension of the vector
    :return:
    """

    import numpy as np

    m = hashlib.md5()
    m.update(text.encode("utf-8"))
    seed = int(m.hexdigest(), 16) % (2**32 - 1)
    np.random.seed(seed)
    vector = np.random.randn(dim)
    norm = np.linalg.norm(vector)
    unit_vector = vector / norm
    unit_vector_list = unit_vector.tolist()
    return unit_vector_list


async def embed_query(query: str, embedding_model: Model, embedding_size: int):
    """
    embed the query text
    :param query: the query text
    :param embedding_model: the embedding_model to use
    :param embedding_size: the embedding size of the model
    :return:
    """

    if CONFIG.DEV:
        return _generate_random_unit_vector(query, embedding_size)

    response = await _inference(embedding_model=embedding_model, input_text_list=[query], input_type="query")
    check_http_error(response)
    return response.json()["data"][0]["embedding"]


async def embed_documents(documents: List[str], embedding_model: Model, embedding_size: int):
    """
    embed the query text
    :param documents: the text list of the documents
    :param embedding_model: the embedding_model to use
    :param embedding_size: the embedding size of the model
    :return:
    """

    if CONFIG.DEV:
        return [_generate_random_unit_vector(text, embedding_size) for text in documents]

    response = await _inference(embedding_model=embedding_model, input_text_list=documents, input_type="document")
    check_http_error(response)
    return [d["embedding"] for d in response.json()["data"]]
