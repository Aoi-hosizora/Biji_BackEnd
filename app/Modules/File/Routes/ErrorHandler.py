from app.Utils import RespUtil, ErrorUtil

from app.Modules.File.Exceptions.FileError import FileError

def register_file_error_handler(error: TypeError):
    '''
    Note 模块的错误处理
    '''
    if isinstance(error, FileError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="File Test Error"),
            code=ErrorUtil.BadRequest
        )
    else:
        return None