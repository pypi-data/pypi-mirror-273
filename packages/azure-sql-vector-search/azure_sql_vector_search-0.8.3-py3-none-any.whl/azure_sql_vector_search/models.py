from enum import StrEnum
from typing import TypedDict


class DistanceMetric(StrEnum):
    COSINE_SIMILARITY = "cosine"
    DOT_PRODUCT = "dot"
    EUCLIDEAN_DISTANCE = "euclidean"


class VectorSearchClientMode(StrEnum):
    NATIVE = "native"
    CLASSIC = "classic"


class VectorSearchResult(TypedDict):
    id: int
    content: str
    metadata: dict[str, object]
    vector_content: list[float]
