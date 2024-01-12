from enum import Enum
from typing import List, Tuple

__all__ = ["SerializePurpose", "Status", "SortOrderEnum", "ListResult"]


class SerializePurpose(int, Enum):
    REDIS = 1
    RESPONSE = 2


class Status(str, Enum):
    CREATING = "creating"
    READY = "ready"
    DELETING = "deleting"
    ERROR = "error"
    PARTIAL = "partial"


class SortOrderEnum(str, Enum):
    DESC = "desc"
    ASC = "asc"


ListResult = Tuple[List, int, bool]
