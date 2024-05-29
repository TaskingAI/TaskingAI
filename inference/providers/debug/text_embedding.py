from provider_dependency.text_embedding import *
from typing import List, Dict, Optional
import hashlib
import numpy as np
import re


def _generate_random_unit_vector(text, dim):
    """
    generate a random unit vector based on the input text
    :param text: the input text
    :param dim: the dimension of the vector
    :return: a random unit vector
    """

    m = hashlib.md5()
    m.update(text.encode("utf-8"))
    seed = int(m.hexdigest(), 16) % (2**32 - 1)
    np.random.seed(seed)
    vector = np.random.randn(dim)
    norm = np.linalg.norm(vector)
    unit_vector = vector / norm
    unit_vector_list = unit_vector.tolist()
    return unit_vector_list


class DebugTextEmbeddingModel(BaseTextEmbeddingModel):
    async def embed_text(
        self,
        provider_model_id: str,
        input: List[str],
        credentials: ProviderCredentials,
        configs: TextEmbeddingModelConfiguration,
        input_type: Optional[TextEmbeddingInputType] = None,
        proxy: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> TextEmbeddingResult:
        match = re.search(r"\d+$", provider_model_id)
        if match:
            dim = int(match.group())
        else:
            dim = 512
        outputs = [{"index": i, "embedding": _generate_random_unit_vector(text, dim)} for i, text in enumerate(input)]
        return TextEmbeddingResult(
            data=[TextEmbeddingOutput(embedding=output["embedding"], index=output["index"]) for output in outputs],
        )
