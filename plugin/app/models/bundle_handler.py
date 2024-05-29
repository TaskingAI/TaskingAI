from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from app.models import BundleCredentials
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class BundleHandler(ABC):

    def __init__(self):
        pass

    @abstractmethod
    async def verify(self, credentials: BundleCredentials):
        raise NotImplementedError
