from enum import Enum


class Type(Enum):
    """
    A metric type.
    """

    General = -1
    Device = 0
    System = 1
    Environment = 2
    Process = 3
    User = 4
