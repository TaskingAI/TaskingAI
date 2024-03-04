import tiktoken
from pydantic import Field
from typing import List
from ._base import Tokenizer, TokenizerType

__all__ = [
    "TiktokenTokenizer",
]


tiktoken_tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")


class TiktokenTokenizer(Tokenizer):
    type: TokenizerType = Field(
        TokenizerType.TIKTOKEN, Literal=TokenizerType.TIKTOKEN, description="The type of the tokenizer."
    )

    def encode(self, text: str) -> List[int]:
        return tiktoken_tokenizer.encode(text)

    def decode(self, tokens: List[int]) -> str:
        return tiktoken_tokenizer.decode(tokens)
