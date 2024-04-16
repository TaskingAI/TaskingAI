from typing import List
from tkhelper.utils import check_http_error
from app.config import CONFIG
from app.models import Model
import hashlib
from app.services.inference.text_embedding import text_embedding


def _generate_random_unit_vector(text, dim):
    """
    generate a random unit vector based on the input text
    :param text: the input text
    :param dim: the dimension of the vector
    :return: a random unit vector
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
    :return: the embedding vector
    """

    if CONFIG.DEV:
        return _generate_random_unit_vector(query, embedding_size)

    response = await text_embedding(
        model=embedding_model,
        encrypted_credentials=embedding_model.encrypted_credentials,
        input_text_list=[query],
        input_type="query",
    )
    check_http_error(response)
    return response.json()["data"][0]["embedding"]


async def embed_documents(documents: List[str], embedding_model: Model, embedding_size: int) -> List[List[float]]:
    """
    embed the query text
    :param documents: the text list of the documents
    :param embedding_model: the embedding_model to use
    :param embedding_size: the embedding size of the model
    :return: a list of embedding vectors
    """

    if CONFIG.DEV:
        return [_generate_random_unit_vector(text, embedding_size) for text in documents]

    response = await text_embedding(
        model=embedding_model,
        encrypted_credentials=embedding_model.encrypted_credentials,
        input_text_list=documents,
        input_type="document",
    )
    check_http_error(response)
    return [d["embedding"] for d in response.json()["data"]]
