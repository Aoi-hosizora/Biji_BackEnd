from app.util import RespUtil, ErrorUtil

from app.module.star.Exceptions.NotExistError import NotExistError
from app.module.star.Exceptions.InsertError import InsertError
from app.module.star.Exceptions.DeleteError import DeleteError
from app.module.star.Exceptions.ExistError import ExistError

def register_star_error_handler(error: TypeError):
    '''
    Star 模块的错误处理
    '''
    if isinstance(error, NotExistError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Not Exist Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, ExistError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Exist Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, InsertError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Insert Error"),
            code=ErrorUtil.NotFound
        )
    elif isinstance(error, DeleteError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Delete Error"),
            code=ErrorUtil.NotFound
        )
    else:
        return None