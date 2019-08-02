from app.Utils import RespUtil, ErrorUtil

from app.Utils.Exceptions.AuthNoneError import AuthNoneError
from app.Utils.Exceptions.BodyFormKeyError import BodyFormKeyError
from app.Utils.Exceptions.BodyRawJsonError import BodyRawJsonError
from app.Utils.Exceptions.QueryError import QueryError

def register_global_error_handler(error: TypeError):
    
    if isinstance(error, AuthNoneError): # 没有认证头
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Auth Token Error"),
            code=ErrorUtil.UnAuthorized
        )
    elif isinstance(error, BodyFormKeyError): # Body form 参数错误
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Body Form Error"),
            code=ErrorUtil.BadRequest
        )
    elif isinstance(error, BodyRawJsonError): # Body json 参数错误
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Body Json Error"),
            code=ErrorUtil.BadRequest
        )
    elif isinstance(error, QueryError): # 查询参数错误
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Query Param Error"),
            code=ErrorUtil.BadRequest
        )
    else:
        return None