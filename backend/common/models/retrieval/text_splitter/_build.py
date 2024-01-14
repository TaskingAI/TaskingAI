from typing import Optional, Dict
from ._base import TextSplitter, TextSplitterType
from .token import TokenTextSplitter


def build_text_splitter(data: Dict) -> Optional[TextSplitter]:
    if not isinstance(data, Dict):
        raise ValueError("Text splitter input data must be a valid dictionary")

    splitter_type = data.get("type")
    if splitter_type is None:
        return None

    # Depending on the type of splitter, initialize the appropriate splitter instance
    if splitter_type == TextSplitterType.TOKEN.value:
        chunk_size = data.get("chunk_size")
        chunk_overlap = data.get("chunk_overlap")
        return TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    else:
        # If the splitter_type is unknown, return None
        return None
