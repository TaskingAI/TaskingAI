from enum import Enum
from abc import abstractmethod
from pydantic import BaseModel, Field
from typing import List


class TextSplitterType(str, Enum):
    """TextSplitterType enum."""

    TOKEN = "token"


class TextSplitter(BaseModel):
    """TextSplitter class."""

    type: TextSplitterType = Field(..., description="The type of the text splitter.")

    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        raise NotImplementedError

    # todo: add title to each chunk
