from app.util import RespUtil, ErrorUtil

from app.controller.file.exception.FileError import FileError

def register_file_error_handler(error: TypeError):
    '''
    File 模块的错误处理
    '''
    if isinstance(error, FileError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="File Test Error"),
            code=ErrorUtil.BadRequest
        )
    else:
        return None