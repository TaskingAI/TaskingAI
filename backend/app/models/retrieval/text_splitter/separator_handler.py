from typing import List, Optional, Tuple

__all__ = [
    "split_text_by_separator",
]


def _separate_text(text: str, separators: List[str]):
    sections = [text]
    for sep in separators:
        new_sections = []
        for section in sections:
            split_sections = section.split(sep)
            new_sections.extend(split_sections)
        sections = new_sections
    return sections


def split_text_by_separator(
    text: str,
    title: Optional[str],
    separators: Optional[List[str]],
    chunk_size: Optional[int],
    chunk_overlap: Optional[int],
) -> Tuple[List[str], List[int]]:
    """
    Split text into chunks. First use the separators to split the text into multiple parts,
     then split each part into chunks using the token text splitter if the part is too long.
    :param text: the text to split
    :param title: the title of the text. If not None, the title will be appended to the beginning of each chunk
    :param separators: the list of separators to split the text
    :param chunk_size: the maximum number of tokens in each text chunk
    :param chunk_overlap: the number of overlapping tokens between adjacent chunks
    :return: a list of tuples (chunk, num_tokens)
    """

    from ..tokenizer import default_tokenizer
    from .token_handler import split_text_by_token

    chunk_size = chunk_size or 1000
    chunk_overlap = chunk_overlap or 0

    sections = _separate_text(text, separators)

    chunks = []
    chunk_num_tokens = []
    for section in sections:
        part = section.strip()
        if part and len(part) > chunk_size:
            section_chunks, section_tokens = split_text_by_token(section, None, chunk_size, chunk_overlap)
            chunks.extend(section_chunks)
            chunk_num_tokens.extend(section_tokens)
        elif part:  # too short
            chunks.append(part)
            chunk_num_tokens.append(default_tokenizer.count_tokens(part))

    if title:
        title_num_tokens = default_tokenizer.count_tokens(title)
        chunks = [f"{title}\n\n{chunk}" for chunk in chunks]
        chunk_num_tokens = [n + title_num_tokens for n in chunk_num_tokens]

    return chunks, chunk_num_tokens
