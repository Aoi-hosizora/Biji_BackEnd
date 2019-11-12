from app.util import RespUtil, ErrorUtil

from app.module.auth.Exceptions.RegisterError import RegisterError
from app.module.auth.Exceptions.UserExistError import UserExistError
from app.module.auth.Exceptions.UserNotExistError import UserNotExistError
from app.module.auth.Exceptions.PasswordFormatError import PasswordFormatError
from app.module.auth.Exceptions.UsernameFormatError import UsernameFormatError
from app.module.auth.Exceptions.TokenTimeoutError import TokenTimeoutError
from app.module.auth.Exceptions.LoginError import LoginError
from app.module.auth.Exceptions.LoginPasswordError import LoginPasswordError
from app.module.auth.Exceptions.LogoutError import LogoutError

def register_auth_error_handler(error: TypeError):
    '''
    Auth 模块的错误处理
    '''
    if isinstance(error, RegisterError): # 注册失败
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Register Error"),
            code=ErrorUtil.NotAcceptable
        )
    elif isinstance(error, UserExistError): # 用户已存在
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="User Exist Error"),
            code=ErrorUtil.NotAcceptable
        )
    elif isinstance(error, UsernameFormatError): # 用户名格式错误
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Username Format Error"),
            code=ErrorUtil.NotAcceptable
        )
    elif isinstance(error, PasswordFormatError): # 密码格式错误
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Password Format Error"),
            code=ErrorUtil.NotAcceptable
        )
    ###############################################################################################
    elif isinstance(error, LoginError): # 登录失败
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Login Error"),
            code=ErrorUtil.UnAuthorized
        )
    elif isinstance(error, LoginPasswordError): # 密码错误
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Password Error"),
            code=ErrorUtil.UnAuthorized
        )
    elif isinstance(error, UserNotExistError): # 用户未存在
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="User Not Exist Error"),
            code=ErrorUtil.UnAuthorized
        )
    elif isinstance(error, TokenTimeoutError): # 登录过期
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Login Timeout"),
            code=ErrorUtil.UnAuthorized
        )
    ###############################################################################################
    elif isinstance(error, LogoutError): # 注销失败
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Logout Error"),
            code=ErrorUtil.NotAcceptable
        )
    else:
        return None