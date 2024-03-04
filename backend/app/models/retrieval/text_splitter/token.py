from ._base import TextSplitter, TextSplitterType
from pydantic import Field, model_validator
from typing import List, Dict, Any, Optional, Tuple
import math
from ..tokenizer import TokenizerType, Tokenizer, get_tokenizer


def _text_split(
    tokenizer: Tokenizer, text: str, title: Optional[str], chunk_size: int, chunk_overlap: int
) -> Tuple[List[str], List[int]]:
    """
    Split text into chunks.
    :param tokenizer: the tokenizer to encode and decode text
    :param text: the text to split
    :param title: the title of the text. If not None, the title will be appended to the beginning of each chunk
    :param chunk_size: the maximum number of tokens in each text chunk
    :param chunk_overlap: the number of overlapping tokens between adjacent chunks
    :return: a list of tuples (chunk, num_tokens)
    """

    if not text:
        return [], []

    document_tokens = tokenizer.encode(text)
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
    chunk_num_tokens = []
    chunk_start = 0
    for i in range(K):
        chunk_end = chunk_start + average_chunk_size

        # ensure the last chunk is not longer than the average chunk size
        chunk_end = min(chunk_end, document_size)

        # get chunk tokens
        chunk_tokens = document_tokens[chunk_start:chunk_end]

        # decode chunk tokens
        new_chunk = tokenizer.decode(chunk_tokens).strip()
        chunks.append(new_chunk)

        chunk_num_tokens.append(len(chunk_tokens))

        # update chunk_start
        chunk_start = chunk_end - min(chunk_overlap, chunk_size)

    title_num_tokens = 0
    if title:
        title_num_tokens = tokenizer.count_tokens(title)

    # append title to each chunk
    for i in range(len(chunks)):
        if title:
            chunks[i] = f"{title}\n\n{chunks[i]}"
            chunk_num_tokens[i] += title_num_tokens

    return chunks, chunk_num_tokens


class TokenTextSplitter(TextSplitter):
    type: TextSplitterType = Field(
        TextSplitterType.TOKEN,
        Literal=TextSplitterType.TOKEN,
        description="The type of the text splitter.",
    )

    tokenizer_type: TokenizerType = Field(
        TokenizerType.TIKTOKEN,
        Literal=TokenizerType.TIKTOKEN,
        description="The type of the tokenizer.",
    )

    chunk_size: int = Field(
        200,
        ge=50,
        le=1000,
        description="The maximum number of tokens in each text chunk.",
    )

    chunk_overlap: int = Field(
        0,
        ge=0,
        le=200,
        description="The number of overlapping tokens between adjacent chunks.",
    )

    # check chunk_overlap <= chunk_size/2
    @model_validator(mode="after")
    def validate_chunk_overlap(cls, data: Any):
        if data.chunk_overlap > data.chunk_size / 2:
            raise ValueError("chunk_overlap must be less than or equal to chunk_size/2")
        return data

    def split_text(self, text: str, title: Optional[str]) -> Tuple[List[str], List[int]]:
        """
        Split the text into chunks.
        :param text: the text to split
        :param title: the title of the text. If not None, the title will be appended to the beginning of each chunk
        :return: a list of tuples (chunk, num_tokens)
        """

        tokenizer = get_tokenizer(self.tokenizer_type)
        return _text_split(
            tokenizer=tokenizer,
            text=text,
            title=title,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            # currently, don't output tokenizer_type
            # "tokenizer_type": self.tokenizer_type.value,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
        }
