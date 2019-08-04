from app.Utils import ErrorUtil, RespUtil
from app.Models.Message import Message

from app.Modules.Log.Exceptions.LogNotFoundError import LogNotFoundError
from app.Modules.Log.Models.Log import Log
from app.Modules.Log.Controllers import LogCtrl

from flask import Blueprint, request
from flask.app import Flask
import json

blue_Log = Blueprint("blue_Log", __name__, url_prefix="/log")
def register_blue_Log(app: Flask):
    '''
    注册日志蓝图 `/log`

    `GET /all` `GET /one/<string>`
    '''
    app.register_blueprint(blue_Log)

@blue_Log.route("/all", methods=['GET'])
def AllLogRoute():
    '''
    获得所有日志路由处理 `GET /all`
    '''
    username = RespUtil.getAuthUser(request.headers)
    logs = LogCtrl.getUserAllLog(username=username)
    return RespUtil.jsonRet(
        dict=Log.toJsonSet(logs), 
        code=ErrorUtil.Success
    )

@blue_Log.route("/one/<string:mod>", methods=['GET'])
def OneLogRoute(mod):
    '''
    获得一个日志路由处理 `GET /one`
    '''
    username = RespUtil.getAuthUser(request.headers)
    if mod.lower() == "note":
        log = LogCtrl.getNoteLog(username=username)
    elif mod.lower() == "group":
        log = LogCtrl.getGroupLog(username=username)
    elif mod.lower() == "star":
        log = LogCtrl.getStarLog(username=username)
    elif mod.lower() == "file":
        log = LogCtrl.getFileLog(username=username)
    elif mod.lower() == "schedule":
        log = LogCtrl.getScheduleLog(username=username)
    else:
        raise LogNotFoundError(mod)
    return RespUtil.jsonRet(
        dict=log.toJson(), 
        code=ErrorUtil.Success
    )