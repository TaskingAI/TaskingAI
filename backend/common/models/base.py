from enum import Enum

__all__ = ["SerializePurpose", "Status"]


class SerializePurpose(int, Enum):
    REDIS = 1
    RESPONSE = 2


class Status(int, Enum):
    CREATING = 0
    READY = 1
    DELETING = 2
    ERROR = 3
    PARTIAL = 4
