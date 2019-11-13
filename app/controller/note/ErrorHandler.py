from app.util import RespUtil, ErrorUtil

from app.controller.note.exception.NotExistError import NotExistError
from app.controller.note.exception.UpdateError import UpdateError
from app.controller.note.exception.InsertError import InsertError
from app.controller.note.exception.DeleteError import DeleteError
from app.controller.note.exception.ExistError import ExistError
from app.controller.note.exception.ImageUploadError import ImageUploadError
from app.controller.note.exception.ImageTypeError import ImageTypeError
from app.controller.note.exception.ImageNotExistError import ImageNotExistError

def register_note_error_handler(error: TypeError):
    '''
    Note 模块的错误处理
    '''
    if isinstance(error, NotExistError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Not Exist Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, UpdateError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Update Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, ExistError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Exist Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, InsertError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Insert Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, DeleteError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Delete Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, ImageUploadError):
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