from enum import Enum


class PathType(Enum):
    UNKNOWN = -1
    FOLDER = 0
    FILE = 1
    rsvd = 2
    HTTP = 3
    SVN = 4
