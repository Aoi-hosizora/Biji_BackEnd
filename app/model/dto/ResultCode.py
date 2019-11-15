from enum import Enum, unique


@unique
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

    BAD_REQUEST = 400, 'Bad Request'
    UNAUTHORIZED = 401, 'Unauthorized'
    FORBIDDEN = 403, 'Forbidden'
    METHOD_NOT_ALLOWED = 405, 'Method Not Allowed'
    NOT_ACCEPTABLE = 406, 'Not Acceptable'
