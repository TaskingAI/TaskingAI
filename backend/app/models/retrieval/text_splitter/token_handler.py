from typing import List, Optional, Tuple
import math
from ..tokenizer import default_tokenizer

__all__ = [
    "split_text_by_token",
]


def split_text_by_token(
    text: str,
    title: Optional[str],
    chunk_size: int,
    chunk_overlap: int,
) -> Tuple[List[str], List[int]]:
    """
    Split text into chunks.
    :param text: the text to split
    :param title: the title of the text. If not None, the title will be appended to the beginning of each chunk
    :param chunk_size: the maximum number of tokens in each text chunk
    :param chunk_overlap: the number of overlapping tokens between adjacent chunks
    :return: a list of tuples (chunk, num_tokens)
    """

    if not text:
        return [], []

    tokenizer = default_tokenizer
    # todo: use different tokenizer

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
