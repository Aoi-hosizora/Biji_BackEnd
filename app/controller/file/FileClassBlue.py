import qrcode

from app.database.dao.ShareCodeDao import ShareCodeDao

from app.util import ErrorUtil, RespUtil
from app.model.dto.Message import Message

from app.controller.file.controller import FileClassCtrl
from app.model.po.FileClass import FileClass

from flask import Blueprint, request, send_file
from flask.app import Flask

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
        data=FileClass.toJsonSet(fileClasses),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_FileClass.route("/update", methods=['Put'])
def UpdateFileClassRoute():
    '''
    更新文件分类路由处理 `PUT /update`
    
    @body `FileClass` JSON
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    fileClass = FileClassCtrl.getFileClassFromReqData(request.get_data(as_text=True))
    
    FileClassCtrl.updateFileClass(username=username, fileClass=fileClass)
    return RespUtil.jsonRet(
        data=fileClass.toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_FileClass.route("/insert", methods=['Post'])
def InsertFileClassRoute():
    '''
    插入文件分类路由处理 `POST /insert`

    @body `FileClass` JSON
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    fileClass = FileClassCtrl.getFileClassFromReqData(request.get_data(as_text=True))

    FileClassCtrl.insertFileClass(username=username, fileClass=fileClass)
    return RespUtil.jsonRet(
        data=fileClass.toJson(),
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
        data=fileClass.toJson(),
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
        data=Message(message="FileClasses push finished", detail=len(fileClasses)).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_FileClass.route("/share", methods=['GET'])
def ShareFilesRoute():
    '''
    生成文件共享二维码和共享码
    :return:
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    foldername = request.args.get('foldername')
    codeJson = FileClassCtrl.shareCode2Json(username=username, foldername=foldername)
    shareCodeDao = ShareCodeDao()
    shareCodeDao.addShareCode(username+foldername, codeJson)
    qrcode.make(data=codeJson).save('temp.png')
    return send_file('temp.png')
