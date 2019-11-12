from app.util import ErrorUtil, RespUtil
from app.model.Message import Message
from app.util.exception.BodyFormKeyError import BodyFormKeyError

from app.module.auth.Exceptions.RegisterError import RegisterError
from app.module.auth.Exceptions.LoginError import LoginError
from app.module.auth.Exceptions.LoginPasswordError import LoginPasswordError
from app.module.auth.Exceptions.LogoutError import LogoutError

from app.module.auth.Models.RegLogInfo import RegLogInfo
from app.module.auth.Controllers import PasswordCtrl

from flask import Blueprint, request
from flask.app import Flask
import json

blue_RegLog = Blueprint("blue_RegLog", __name__, url_prefix="/auth")
def register_blue_RegLog(app: Flask):
    '''
    注册登录注册蓝图 `/auth`

    `POST /login` `POST /register`
    '''
    app.register_blueprint(blue_RegLog)


@blue_RegLog.route("/login", methods=['POST'])
def LoginRoute():
    '''
    登录路由处理 `POST /login`
    '''
    try:
        postjson = json.loads(request.get_data(as_text=True))
    except:
        raise BodyFormKeyError()

    nonePostKeys = [
        key for key in ['username', 'password']
        if key not in postjson or postjson[key] == None or str.strip(postjson[key]) == ""
    ]
    if not len(nonePostKeys) == 0:
        raise(BodyFormKeyError(nonePostKeys))
        
    username = str.strip(postjson['username'])
    password = str.strip(postjson['password'])
    try:
        expiration = postjson['expiration']
    except:
        expiration = 0

    ok, token = PasswordCtrl.Login(username, password, expiration)
    if ok:
        return RespUtil.jsonRet(
            data=RegLogInfo(username, isLogin=True).toJson(),
            code=ErrorUtil.Success,
            headers={ 'Authorization': token }
        )
    else:
        # 密码不一致 或者 redis 插入错误
        raise(LoginPasswordError(username))

@blue_RegLog.route("/register", methods=['POST'])
def RegisterRoute():
    '''
    注册路由处理 `POST /register`
    '''
    try:
        postjson = json.loads(request.get_data(as_text=True))
    except:
        raise BodyFormKeyError()

    nonePostKeys = [
        key for key in ['username', 'password']
        if key not in postjson or postjson[key] == None or str.strip(postjson[key]) == ""
    ]
    if not len(nonePostKeys) == 0:
        raise(BodyFormKeyError(nonePostKeys))
        
    username = str.strip(postjson['username'])
    password = str.strip(postjson['password'])
    
    if PasswordCtrl.Register(username, password):
        return RespUtil.jsonRet(
            data=RegLogInfo(username, isLogin=False).toJson(),
            code=ErrorUtil.Success
        )
    else:
        raise(RegisterError(username))

@blue_RegLog.route("/logout", methods=['POST'])
def LogoutRoute():
    '''
    注销路由处理 `POST /logout`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    PasswordCtrl.Logout(username)
    return RespUtil.jsonRet(
        data=Message("Logout Success").toJson(),
        code=ErrorUtil.Success
    )