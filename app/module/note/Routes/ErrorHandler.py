from app.util import RespUtil, ErrorUtil

from app.module.note.Exceptions.NotExistError import NotExistError
from app.module.note.Exceptions.UpdateError import UpdateError
from app.module.note.Exceptions.InsertError import InsertError
from app.module.note.Exceptions.DeleteError import DeleteError
from app.module.note.Exceptions.ExistError import ExistError
from app.module.note.Exceptions.ImageUploadError import ImageUploadError
from app.module.note.Exceptions.ImageTypeError import ImageTypeError
from app.module.note.Exceptions.ImageNotExistError import ImageNotExistError

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