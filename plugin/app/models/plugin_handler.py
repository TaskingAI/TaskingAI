from abc import ABC, abstractmethod
from typing import Dict, Optional
from app.models import BundleCredentials
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class PluginOutput(BaseModel):
    status: int = Field(200)
    data: Dict = Field({})


class PluginInput(BaseModel):
    input_params: Dict = Field(...)
    project_id: Optional[str] = Field(None)


class PluginHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def execute(
        self,
        credentials: BundleCredentials,
        plugin_input: PluginInput,
    ) -> PluginOutput:
        raise NotImplementedError
