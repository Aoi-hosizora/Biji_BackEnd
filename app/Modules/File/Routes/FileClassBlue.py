from app.Utils import ErrorUtil, RespUtil
from app.Models.Message import Message
from app.Utils.Exceptions.BodyRawJsonError import BodyRawJsonError
from app.Utils.Exceptions.QueryError import QueryError

from app.Modules.File.Controllers import FileClassCtrl
from app.Modules.File.Models.FileClass import FileClass

from flask import Blueprint, request
from flask.app import Flask
import json

blue_FileClass = Blueprint("blue_FileClass", __name__, url_prefix="/fileclass")
def register_blue_FileClass(app: Flask):
    '''
    注册文件分类蓝图 `/fileclass`

    `GET /all` `GET /one?id=<int>`
    `POST /update` `PUT /insert` `DELETE /delete`
    '''
    app.register_blueprint(blue_FileClass)

@blue_FileClass.route("/all", methods=['GET'])
def AllFileClassRoute():
    '''
    获得所有文件分类路由处理 `GET /all`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    fileClasses = FileClassCtrl.getAllFileClasses(username=username)
    return RespUtil.jsonRet(
        dict=FileClass.toJsonSet(fileClasses),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_FileClass.route("/one", methods=['GET'])
def OneGroupRoute():
    '''
    获得单个文件分类路由处理 `GET /one?id=<int>`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    id = request.args.get('id')
    try:
        id = int(id)
    except:
        raise QueryError(list(['id']))
        
    fileClasses = FileClassCtrl.getOneFileClass(username=username, id=id)
    return RespUtil.jsonRet(
        dict=fileClasses.toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_FileClass.route("/update", methods=['Post'])
def UpdateFileClassRoute():
    '''
    更新文件分类路由处理 `POST /update`
    
    @body `FileClass` JSON
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    fileClass = FileClassCtrl.getFileClassesFromReqData(request.get_data(as_text=True))
    
    FileClassCtrl.updateFileClass(username=username, fileClass=fileClass)
    return RespUtil.jsonRet(
        dict=fileClass.toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_FileClass.route("/insert", methods=['Put'])
def InsertFileClassRoute():
    '''
    插入文件分类路由处理 `POST /insert`

    @body `FileClass` JSON
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    fileClass = FileClassCtrl.getFileClassFromReqData(request.get_data(as_text=True))
    
    FileClassCtrl.insertFileClass(username=username, fileClass=fileClass)
    return RespUtil.jsonRet(
        dict=fileClass.toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_FileClass.route("/delete", methods=['Delete'])
def DeleteFileClasspRoute():
    '''
    删除文件分类路由处理 `POST /delete`

    @body `FileClass` JSON
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    fileClass = FileClassCtrl.getFileClassFromReqData(request.get_data(as_text=True))

    FileClassCtrl.deleteFileClass(username=username, fileClass=fileClass)
    return RespUtil.jsonRet(
        dict=fileClass.toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_FileClass.route("/push", methods=['POST'])
def PushFileClassRoute():
    '''
    同步文件分类路由处理 `POST /push`

    @body `FileClass []` JSON
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    fileClasses = FileClassCtrl.getFileClassesFromReqData(request.get_data(as_text=True))

    FileClassCtrl.pushFileClass(username, fileClasses)
    return RespUtil.jsonRet(
        dict=Message(message="FileClasses push finished", detail=len(fileClasses)).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )