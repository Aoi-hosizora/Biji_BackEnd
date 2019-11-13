from enum import Enum


class ResultCode(Enum):
    """
    Http 状态返回码
    """

    def __init__(self, code, message):
        self.code = code
        self.message = message

    SUCCESS = 200, 'Success'
    NOT_FOUND = 404, 'Not Found'
    INTERNAL_SERVER_ERROR = 500, 'Internal Server Error'
