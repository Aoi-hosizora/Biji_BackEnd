from app.Utils import ErrorUtil, RespUtil
from app.Models.Message import Message

from app.Modules.File.Controllers import FileCtrl
from app.Modules.File.Models.File import File

from flask import Blueprint, request, send_file
from flask.app import Flask

import os


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
        dict=File.toJsonSet(files),
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

    file = FileCtrl.getOneFile(username=username, foldername=foldername, filename=filename)
    filepath = file.filepath

    return send_file(filepath)


@blue_File.route("/upload", methods=['POST'])
def UploadFileRoute():
    '''

    上传文件路由处理 `POST /upload`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    form = request.form
    id = form['id']
    foldername = form['foldername']
    file = request.files['file']
    if file != None:
        filename, filepath = FileCtrl.saveFile(file=file, username=username)
        file = File(username, id, foldername, filename, filepath)
        FileCtrl.insertFile(username=username, file=file)
        return RespUtil.jsonRet(
            dict=Message(
                message="File upload success",
                detail=file.filename
            ).toJson(),
            code=ErrorUtil.Success,
            headers={'Authorization': newToken} if newToken != "" else {}
        )
    return RespUtil.jsonRet(
        dict=Message(
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
    form = request.form
    id = form['id']
    foldername = form['foldername']
    filename = form['filename']

    FileCtrl.deleteFile(username, File(username, id, foldername, filename, ''))
    return RespUtil.jsonRet(
        dict=Message(
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
    form = request.form
    foldername = form['foldername']

    FileCtrl.deleteFileByClass(username, foldername)
    return RespUtil.jsonRet(
        dict=Message(
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
    files = FileCtrl.getDocumentsFromReqData(request.get_data(as_text=True))

    FileCtrl.pushFile(username, files)
    return RespUtil.jsonRet(
        dict=Message(message="Files push finished", detail=len(files)).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )