from app.Utils import RespUtil, ErrorUtil

from app.Utils.Exceptions.PostFormKeyError import PostFormKeyError
from app.Utils.Exceptions.QueryError import QueryError

def register_global_error_handler(error: TypeError):
    if isinstance(error, PostFormKeyError): # Post 参数错误
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Post Form Key Error"),
            code=ErrorUtil.BadRequest
        )
    elif isinstance(error, QueryError): # 查询参数错误
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Request Query Param Error"),
            code=ErrorUtil.BadRequest
        )
    else:
        return None