from app.util import ErrorUtil, RespUtil
from app.model.dto.Message import Message
from app.route.exception.BodyFormKeyError import BodyFormKeyError

from app.controller.auth.exception.RegisterError import RegisterError
from app.controller.auth.exception.LoginPasswordError import LoginPasswordError

from app.model.dto.RegLogInfo import RegLogInfo
from app.controller.auth.Controllers import AuthCtrl

from flask import Blueprint, request
from flask.app import Flask
import json

blue_Auth = Blueprint("blue_Auth", __name__, url_prefix="/auth")
def register_blue_Auth(app: Flask):
    '''
    注册登录注册蓝图 `/auth`

    `POST /login` `POST /register`
    '''
    app.register_blueprint(blue_Auth)


@blue_Auth.route("/login", methods=['POST'])
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

    ok, token = AuthCtrl.Login(username, password, expiration)
    if ok:
        return RespUtil.jsonRet(
            data=RegLogInfo(username, isLogin=True).toJson(),
            code=ErrorUtil.Success,
            headers={ 'Authorization': token }
        )
    else:
        # 密码不一致 或者 redis 插入错误
        raise(LoginPasswordError(username))

@blue_Auth.route("/register", methods=['POST'])
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
    
    if AuthCtrl.Register(username, password):
        return RespUtil.jsonRet(
            data=RegLogInfo(username, isLogin=False).toJson(),
            code=ErrorUtil.Success
        )
    else:
        raise(RegisterError(username))

@blue_Auth.route("/logout", methods=['POST'])
def LogoutRoute():
    '''
    注销路由处理 `POST /logout`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    AuthCtrl.Logout(username)
    return RespUtil.jsonRet(
        data=Message("Logout Success").toJson(),
        code=ErrorUtil.Success
    )