from app.Utils import RespUtil, ErrorUtil

from app.Modules.Note.Exceptions.NotExistError import NotExistError
from app.Modules.Note.Exceptions.UpdateError import UpdateError
from app.Modules.Note.Exceptions.InsertError import InsertError
from app.Modules.Note.Exceptions.DeleteError import DeleteError
from app.Modules.Note.Exceptions.ExistError import ExistError
from app.Modules.Note.Exceptions.ImageUploadError import ImageUploadError
from app.Modules.Note.Exceptions.ImageTypeError import ImageTypeError
from app.Modules.Note.Exceptions.ImageNotExistError import ImageNotExistError

def register_note_error_handler(error: TypeError):
    '''
    Note 模块的错误处理
    '''
    if isinstance(error, NotExistError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Not Exist Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, UpdateError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Update Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, ExistError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Exist Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, InsertError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Insert Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, DeleteError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Delete Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, ImageUploadError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Image Upload Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, ImageTypeError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Image Type Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, ImageNotExistError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Image Not Exist Error"),
            code=ErrorUtil.NotFound
        )
    else:
        return None