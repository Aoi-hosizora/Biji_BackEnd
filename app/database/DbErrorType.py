from enum import Enum, unique


@unique
class DbErrorType(Enum):
    """
    数据库操作后的状态枚举
    """

    SUCCESS = 0
    NOT_FOUND = 1  # Update & Delete
    FOUNDED = 2  # Insert
    FAILED = 3  # Operate Rollback
