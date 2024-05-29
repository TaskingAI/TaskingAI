from pydantic import BaseModel, Field


__all__ = ["Document", "RerankDocument", "RerankResult", "RerankUsage"]


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


class RerankResult(BaseModel):
    """
    Model class for rerank result.
    """

    results: list[RerankDocument] = Field(
        ...,
        description="The list of rerank documents.",
        examples=[
            [
                {
                    "index": 3,
                    "document": {"text": "Natural organic skincare range for sensitive skin"},
                    "relevance_score": 0.8292155861854553,
                },
                {
                    "index": 2,
                    "document": {"text": "Organic cotton baby clothes for sensitive skin"},
                    "relevance_score": 0.14426936209201813,
                },
                {
                    "index": 6,
                    "document": {"text": "Sensitive skin-friendly facial cleansers and toners"},
                    "relevance_score": 0.13857832551002502,
                },
            ]
        ],
    )


class RerankUsage(BaseModel):
    """
    Model class for usage details.
    """

    input_tokens: int
    output_tokens: int
