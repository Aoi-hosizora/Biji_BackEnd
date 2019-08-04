from app.Utils import RespUtil, ErrorUtil

from app.Modules.Log.Exceptions.LogNotFoundError import LogNotFoundError

def register_log_error_handler(error: TypeError):
    '''
    Log 模块的错误处理
    '''
    if isinstance(error, LogNotFoundError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Log Not Found Error"),
            code=ErrorUtil.NotFound
        )
    else:
        return None