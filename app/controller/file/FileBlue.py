import json

from app.util import ErrorUtil, RespUtil
from app.model.dto.Message import Message

from app.controller.file.controller import FileClassCtrl, FileCtrl
from app.model.po.File import File
from app.model.po.FileClass import FileClass

from flask import Blueprint, request, send_file
from flask.app import Flask

blue_File = Blueprint("blue_File", __name__, url_prefix="/file")

def register_blue_File(app: Flask):
    app.register_blueprint(blue_File)

@blue_File.route("/all", methods=['GET'])
def AllFileRoute():
    '''
    获得目录下所有文件路由处理 `GET /all?foldername=<str>`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    foldername = request.args.get('foldername', '')
    if foldername == '':
        files = FileCtrl.getAllFilesByUsername(username=username)
    else:
        files = FileCtrl.getAllFiles(username=username, foldername=foldername)
    return RespUtil.jsonRet(
        data=File.toJsonSet(files),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_File.route("/download", methods=['GET'])
def DownloadFileRoute():
    '''
    下载文件路由处理 `GET /download?foldername=<str>&filename=<str>`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    foldername = request.args.get('foldername')
    filename = request.args.get('filename')
    id = request.args.get('id')

    file = FileCtrl.getOneFile(username=username, foldername=foldername, filename=filename, id=id)
    filepath = file.filepath

    return send_file(filepath)

@blue_File.route("/upload", methods=['POST'])
def UploadFileRoute():
    '''

    上传文件路由处理 `POST /upload`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    form = request.form
    try:
        id = form['id']
        foldername = form['foldername']
        file = request.files['file']
    except Exception as ex:
        print(ex)
        return ''
    if file != None:
        filename, filepath = FileCtrl.saveFile(file=file, username=username)
        file = File(username, id, foldername, filename, filepath)
        FileCtrl.insertFile(username=username, file=file)
        return RespUtil.jsonRet(
            data=Message(
                message="File upload success",
                detail=file.filename
            ).toJson(),
            code=ErrorUtil.Success,
            headers={'Authorization': newToken} if newToken != "" else {}
        )
    return RespUtil.jsonRet(
        data=Message(
            message="File upload fail",
        ).toJson(),
        code=ErrorUtil.BadRequest,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_File.route("/delete", methods=['DELETE'])
def DeleteFileRoute():
    '''
    删除文件路由处理 `DELETE /delete`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    print(request.get_data(as_text=True))
    form = json.loads(request.get_data(as_text=True))
    id = form['id']
    foldername = form['foldername']
    filename = form['filename']

    FileCtrl.deleteFile(username, File(username, id, foldername, filename, ''))
    return RespUtil.jsonRet(
        data=Message(
            message="File delete success",
            detail=filename
        ).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_File.route("/delete_all", methods=['DELETE'])
def DeleteFileByClassRoute():
    '''
    删除文件路由处理 `DELETE /delete_all`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    foldername = json.loads(request.get_data(as_text=True))['foldername']

    FileCtrl.deleteFileByClass(username, foldername)
    return RespUtil.jsonRet(
        data=Message(
            message="Files delete success",
            detail=foldername
        ).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_File.route("/push", methods=['POST'])
def PushFileRoute():
    '''
    同步文件路由处理 `POST /push`

    @body `File []` JSON
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    files = FileCtrl.getDocumentsFromReqData(username, request.get_data(as_text=True))

    FileCtrl.pushFile(username, files)
    return RespUtil.jsonRet(
        data=Message(message="Files push finished", detail=len(files)).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_File.route("/get_share", methods=['GET'])
def GetSharedFiles():
    '''
    获取共享的文件
    :return:
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    usernameShared = request.args.get('username')
    foldernameShared = request.args.get('foldername')

    shareCodeJson = FileClassCtrl.shareCode2Json(usernameShared, foldernameShared)

    if FileCtrl.checkShareCode(usernameShared + foldernameShared, shareCodeJson):
        
        fileClass = FileClassCtrl.getOneFileClass(usernameShared, FileClass(0, foldernameShared))
        files = FileCtrl.getAllFiles(usernameShared, foldernameShared)
        for file in files:
            file.username = username
        if FileClassCtrl.getOneFileClass(username, fileClass) is None:
            FileClassCtrl.insertFileClass(username, fileClass)
        FileCtrl.pushFile(username, files)

        return RespUtil.jsonRet(
            data=Message(
            message="Get share files success",
        ).toJson(),
            code=ErrorUtil.Success,
            headers={'Authorization': newToken} if newToken != "" else {}
        )
    return RespUtil.jsonRet(
        data=Message(
            message="Get share files fail",
        ).toJson(),
        code=ErrorUtil.NotFound,
        headers={'Authorization': newToken} if newToken != "" else {}
    )
