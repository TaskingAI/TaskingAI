from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from app.models import ProviderCredentials
import logging
from .text_embedding import *
from .model_config import TextEmbeddingModelConfiguration
from app.error import raise_http_error, ErrorCode, raise_provider_api_error

logger = logging.getLogger(__name__)

__all__ = [
    "BaseTextEmbeddingModel",
]


class BaseTextEmbeddingModel(ABC):
    def __init__(self):
        pass

    @staticmethod
    async def handle_response(response):
        """
        Handles the HTTP response, raising specific errors based on the response status and error type.
        """
        if response.status >= 500:
            logger.error(f"response: {response}")
            raise_http_error(ErrorCode.PROVIDER_ERROR, "Provider's service is unavailable")
        if response.status != 200:
            try:
                result = await response.json()
            except Exception:
                result = await response.text()

            raise_provider_api_error(str(result))

    @abstractmethod
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
        raise NotImplementedError
