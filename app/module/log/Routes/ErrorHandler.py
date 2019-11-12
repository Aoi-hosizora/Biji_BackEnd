from app.util import RespUtil, ErrorUtil

from app.module.log.Exceptions.LogNotFoundError import LogNotFoundError

def register_log_error_handler(error: TypeError):
    '''
    Log 模块的错误处理
    '''
    if isinstance(error, LogNotFoundError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Log Not Found Error"),
            code=ErrorUtil.NotFound
        )
    else:
        return None