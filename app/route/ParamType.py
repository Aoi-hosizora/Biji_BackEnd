from enum import Enum, unique
from types import TracebackType
from typing import Optional


@unique
class ParamType(Enum):
    """
    预定义的请求参数类型
    """
    QUERY = 0  # 查询参数错误
    ROUTE = 1  # 路由参数错误
    FORM = 2  # FormData 参数错误
    RAW = 3  # RawJson 参数错误


class ParamError(Exception):
    """
    请求参数错误，返回 400
    """

    def __init__(self, paramType: ParamType) -> None:
        super().__init__()
        self.paramType = paramType

    def with_traceback(self, tb: Optional[TracebackType]) -> BaseException:
        return super().with_traceback(tb)
