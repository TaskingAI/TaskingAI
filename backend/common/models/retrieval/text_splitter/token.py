from ._base import TextSplitter, TextSplitterType
from pydantic import Field, model_validator
from typing import List, Dict, Any
from enum import Enum
import tiktoken
import math

tiktoken_tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")


def tiktoken_text_split(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    if not text:
        return []

    document_tokens = tiktoken_tokenizer.encode(text)
    document_size = len(document_tokens)

    # the number of chunks
    K = math.ceil((document_size - chunk_overlap) / (chunk_size - chunk_overlap))
    if K == 0:
        K = 1

    # the average chunk size
    average_chunk_size = math.ceil((document_size - chunk_overlap) / K) + chunk_overlap

    # the number of chunks that are shorter than the average chunk size
    shorter_chunk_number = K * average_chunk_size - (document_size + chunk_overlap * (K - 1))

    # the number of chunks that are equal to the average chunk size
    standard_chunk_number = K - shorter_chunk_number

    chunks = []
    chunk_start = 0
    for i in range(K):
        chunk_end = chunk_start + average_chunk_size

        # ensure the last chunk is not longer than the average chunk size
        chunk_end = min(chunk_end, document_size)

        # get chunk tokens
        chunk = document_tokens[chunk_start:chunk_end]

        # decode chunk tokens
        new_chunk = tiktoken_tokenizer.decode(chunk).strip()
        chunks.append(new_chunk)

        # update chunk_start
        chunk_start = chunk_end - min(chunk_overlap, chunk_size)

    return chunks


class TokenizerType(str, Enum):
    TIKTOKEN = "tiktoken"


class TokenTextSplitter(TextSplitter):
    type: TextSplitterType = Field(
        TextSplitterType.TOKEN, Literal=TextSplitterType.TOKEN, description="The type of the text splitter."
    )

    tokenizer_type: TokenizerType = Field(
        TokenizerType.TIKTOKEN, Literal=TokenizerType.TIKTOKEN, description="The type of the tokenizer."
    )

    chunk_size: int = Field(200, ge=50, le=1000, description="The maximum number of tokens in each text chunk.")

    chunk_overlap: int = Field(0, ge=0, le=200, description="The number of overlapping tokens between adjacent chunks.")

    # check chunk_overlap <= chunk_size/2
    @model_validator(mode="after")
    def validate_chunk_overlap(cls, data: Any):
        if data.chunk_overlap > data.chunk_size / 2:
            raise ValueError("chunk_overlap must be less than or equal to chunk_size/2")
        return data

    def split_text(self, text: str) -> List[str]:
        if self.tokenizer_type == TokenizerType.TIKTOKEN:
            return tiktoken_text_split(text, self.chunk_size, self.chunk_overlap)
        else:
            raise NotImplementedError

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            # currently, don't output tokenizer_type
            # "tokenizer_type": self.tokenizer_type.value,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
        }
