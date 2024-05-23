from pydantic import BaseModel

__all__ = ["RerankDocument", "RerankResult", "RerankUsage", "Document"]


class Document(BaseModel):
    """
    Model class for the document details.
    """

    text: str


class RerankDocument(BaseModel):
    """
    Model class for rerank document.
    """

    index: int
    document: Document
    relevance_score: float


class RerankUsage(BaseModel):
    """
    Model class for usage details.
    """

    input_tokens: int
    output_tokens: int


class RerankResult(BaseModel):
    """
    Model class for rerank result.
    """

    results: list[RerankDocument]
