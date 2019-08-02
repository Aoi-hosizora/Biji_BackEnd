from app.Utils import RespUtil, ErrorUtil

from app.Utils.Exceptions.BodyFormKeyError import BodyFormKeyError
from app.Utils.Exceptions.BodyRawJsonError import BodyRawJsonError
from app.Utils.Exceptions.QueryError import QueryError

def register_global_error_handler(error: TypeError):
    if isinstance(error, BodyFormKeyError): # Body form 参数错误
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Body Form Key Error"),
            code=ErrorUtil.BadRequest
        )
    elif isinstance(error, BodyRawJsonError): # Body json 参数错误
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Body Raw Json Error"),
            code=ErrorUtil.BadRequest
        )
    elif isinstance(error, QueryError): # 查询参数错误
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Request Query Param Error"),
            code=ErrorUtil.BadRequest
        )
    else:
        return None