from enum import Enum, unique


class DbErrorType(Enum):
    """
    数据库操作后的状态枚举
    """

    SUCCESS = 0
    NOT_FOUND = 1
    FOUNDED = 2
    FAILED = 3
