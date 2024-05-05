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
    SEPARATOR = "separator"


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

    separators: Optional[List[str]] = Field(
        None,
        min_items=1,
        max_items=16,
        description="The list of separators to split the text.",
    )

    def split_text(self, text: str, title: Optional[str]) -> Tuple[List[str], List[int]]:
        """
        Split the text into chunks.
        :param text: the text to split
        :param title: the title of the text. If not None, the title will be appended to the beginning of each chunk
        :return: a list of tuples (chunk, num_tokens)
        """

        from .token_handler import split_text_by_token
        from .separator_handler import split_text_by_separator

        if self.type == TextSplitterType.TOKEN:
            return split_text_by_token(
                text=text,
                title=title,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
            )

        if self.type == TextSplitterType.SEPARATOR:
            return split_text_by_separator(
                text=text,
                title=title,
                separators=self.separators,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
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

        if data.type == TextSplitterType.SEPARATOR:
            if data.separators is None or len(data.separators) == 0:
                raise ValueError("The separators cannot be empty for the separator text splitter.")

            # ensure no empty separator
            if any(not sep for sep in data.separators):
                raise ValueError("The separators field cannot contain empty strings.")

            # ensure each separator is not a substring of another separator
            for i, sep in enumerate(data.separators):
                for j, other_sep in enumerate(data.separators):
                    if i != j and sep in other_sep:
                        raise ValueError(f"Separator '{sep}' is a substring of '{other_sep}'.")

            # ensure the length of each separator is less than 50
            if any(len(sep) >= 50 for sep in data.separators):
                raise ValueError("The length of each separator must be less than 50.")

        if data.chunk_overlap is not None and data.chunk_size is not None and data.chunk_overlap > data.chunk_size / 2:
            raise ValueError("chunk_overlap must be less than or equal to chunk_size/2")

        return data
