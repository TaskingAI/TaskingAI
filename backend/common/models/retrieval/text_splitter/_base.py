from enum import Enum
from abc import abstractmethod
from pydantic import BaseModel, Field
from typing import List, Tuple
from typing import Optional


class TextSplitterType(str, Enum):
    """TextSplitterType enum."""

    TOKEN = "token"


class TextSplitter(BaseModel):
    """TextSplitter class."""

    type: TextSplitterType = Field(..., description="The type of the text splitter.")

    @abstractmethod
    def split_text(self, text: str, title: Optional[str]) -> Tuple[List[str], List[int]]:
        """
        Split the text into chunks.
        :param text: the text to split
        :param title: the title of the text. If not None, the title will be appended to the beginning of each chunk
        :return: a list of tuples (chunk, num_tokens)
        """

        raise NotImplementedError
