from enum import Enum
from abc import abstractmethod
from pydantic import BaseModel, Field
from typing import List

__all__ = [
    "TokenizerType",
    "Tokenizer",
    "get_tokenizer",
    "default_tokenizer",
]


class TokenizerType(str, Enum):
    TIKTOKEN = "tiktoken"


class Tokenizer(BaseModel):
    """Tokenizer class."""

    type: TokenizerType = Field(..., description="The type of the tokenizer.")

    @abstractmethod
    def encode(self, text: str) -> List[int]:
        raise NotImplementedError

    @abstractmethod
    def decode(self, tokens: List[int]) -> str:
        raise NotImplementedError

    def count_tokens(self, text: str) -> int:
        if not text or not isinstance(text, str):
            return 0
        return len(self.encode(text))


tokenizers = {}


def get_tokenizer(type: TokenizerType):
    if tokenizers.get(type):
        return tokenizers[type]

    if type == TokenizerType.TIKTOKEN:
        from .tiktoken import TiktokenTokenizer

        tokenizer = TiktokenTokenizer()
    else:
        raise NotImplementedError

    tokenizers[type] = tokenizer
    return tokenizer


default_tokenizer = get_tokenizer(TokenizerType.TIKTOKEN)
