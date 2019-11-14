from app.util import RespUtil, ErrorUtil

from app.controller.note.exception.ImageUploadError import ImageUploadError
from app.controller.note.exception.ImageTypeError import ImageTypeError
from app.controller.note.exception.ImageNotExistError import ImageNotExistError


def register_note_error_handler(error: TypeError):
    """
    Note 模块的错误处理
    """
    if isinstance(error, ImageUploadError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Image Upload Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, ImageTypeError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Image Type Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, ImageNotExistError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Image Not Exist Error"),
            code=ErrorUtil.NotFound
        )
    else:
        return None
