from enum import Enum, unique


@unique
class ResultCode(Enum):
    """
    Http 状态返回码
    """

    def __init__(self, code, message):
        self.code = code
        self.message = message

    # HTTP 状态码
    SUCCESS = 200, 'Success'
    UNAUTHORIZED = 401, 'Unauthorized'
    NOT_FOUND = 404, 'Not Found'
    INTERNAL_SERVER_ERROR = 500, 'Internal Server Error'

    BAD_REQUEST = 400, 'Bad Request'
    FORBIDDEN = 403, 'Forbidden'
    METHOD_NOT_ALLOWED = 405, 'Method Not Allowed'
    NOT_ACCEPTABLE = 406, 'Not Acceptable'

    # 自定义错误码
    DATABASE_FAILED = 600, 'Database Failed'
    HAS_EXISTED = 601, 'Has Existed'
    DUPLICATE_FAILED = 602, 'Data Duplicate Failed'
    DEFAULT_FAILED = 603, 'Modified Default Failed'
    SAVE_FILE_FAILED = 604, 'Save File Failed'
    SHARE_DOCUMENT_NULL = 605, 'Share Document Null'
