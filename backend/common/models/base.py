from enum import Enum


class ReleaseStatus(int, Enum):
    draft = 0
    alpha_test = 1
    beta_test = 2
    released = 3


class Status(int, Enum):
    CREATING = 0
    READY = 1
    DELETING = 2
    ERROR = 3
    PARTIAL = 4
