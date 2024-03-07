from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Tuple

__all__ = [
    "TextSplitterType",
    "TextSplitter",
]


class TextSplitterType(str, Enum):
    """TextSplitterType enum."""

    TOKEN = "token"


class TextSplitter(BaseModel):
    """TextSplitter class."""

    type: TextSplitterType = Field(..., description="The type of the text splitter.")

    chunk_size: Optional[int] = Field(
        None,
        ge=50,
        le=1000,
        description="The maximum number of tokens in each text chunk.",
    )

    chunk_overlap: Optional[int] = Field(
        None,
        ge=0,
        le=200,
        description="The number of overlapping tokens between adjacent chunks.",
    )

    def split_text(self, text: str, title: Optional[str]) -> Tuple[List[str], List[int]]:
        """
        Split the text into chunks.
        :param text: the text to split
        :param title: the title of the text. If not None, the title will be appended to the beginning of each chunk
        :return: a list of tuples (chunk, num_tokens)
        """

        from .token_handler import split_text_by_token

        if self.type == TextSplitterType.TOKEN:
            return split_text_by_token(
                text=text, title=title, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
            )

        else:
            raise NotImplementedError

    @model_validator(mode="after")
    def validate_model(cls, data):
        if data.type == TextSplitterType.TOKEN:
            if data.chunk_overlap is None:
                raise ValueError("The chunk_overlap field is required for the token text splitter.")

            if data.chunk_size is None:
                raise ValueError("The chunk_size field is required for the token text splitter.")

            if data.chunk_overlap > data.chunk_size / 2:
                raise ValueError("chunk_overlap must be less than or equal to chunk_size/2")

        return data
