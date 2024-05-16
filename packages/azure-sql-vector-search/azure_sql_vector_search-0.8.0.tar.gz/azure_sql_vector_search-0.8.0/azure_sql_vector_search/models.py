from enum import StrEnum


class DistanceMetric(StrEnum):
    COSINE_SIMILARITY = "cosine"
    DOT_PRODUCT = "dot"
    EUCLIDEAN_DISTANCE = "euclidean"


class VectorSearchClientMode(StrEnum):
    NATIVE = "native"
    CLASSIC = "classic"
