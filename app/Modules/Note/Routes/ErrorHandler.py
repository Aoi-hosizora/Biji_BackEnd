from app.Utils import RespUtil, ErrorUtil

from app.Modules.Note.Exceptions.NoteNotExistError import NoteNotExistError
from app.Modules.Note.Exceptions.NoteUpdateError import NoteUpdateError
from app.Modules.Note.Exceptions.NoteInsertError import NoteInsertError
from app.Modules.Note.Exceptions.NoteDeleteError import NoteDeleteError
from app.Modules.Note.Exceptions.NoteExistError import NoteExistError

def register_note_error_handler(error: TypeError):
    '''
    Note 模块的错误处理
    '''
    if isinstance(error, NoteNotExistError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Note Not Exist Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, NoteUpdateError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Note Update Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, NoteExistError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Note Exist Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, NoteInsertError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Note Insert Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, NoteDeleteError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Note Delete Error"),
            code=ErrorUtil.NotFound
        )
    else:
        return None