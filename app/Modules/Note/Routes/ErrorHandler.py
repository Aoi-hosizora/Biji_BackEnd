from app.Utils import RespUtil, ErrorUtil

from app.Modules.Note.Exceptions.NoteError import NoteError

def register_note_error_handler(error: TypeError):
    '''
    Note 模块的错误处理
    '''
    if isinstance(error, NoteError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Note Test Error"),
            code=ErrorUtil.BadRequest
        )
    else:
        return None