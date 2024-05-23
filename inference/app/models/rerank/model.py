from abc import ABC, abstractmethod
from typing import List
from app.models import ProviderCredentials
import logging
from .rerank import *
from app.error import raise_http_error, ErrorCode, raise_provider_api_error

logger = logging.getLogger(__name__)

__all__ = [
    "BaseRerankModel",
]


class BaseRerankModel(ABC):
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
    async def rerank(
        self,
        provider_model_id: str,
        credentials: ProviderCredentials,
        query: str,
        documents: List[str],
        top_n: int,
    ) -> RerankResult:
        raise NotImplementedError
