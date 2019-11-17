import os

from flask import Blueprint, g, request
from flask_httpauth import HTTPTokenAuth
from werkzeug.utils import secure_filename

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.dao.DocumentDao import DocumentDao
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.model.po.Document import Document
from app.route.ParamType import ParamError, ParamType
from app.util import FileUtil


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/document`
    """

    @blue.route('/', methods=['GET'])
    @auth.login_required
    def GetAllRoute():
        """ 所有文档 """
        documents = DocumentDao().queryAllDocuments(g.user)
        return Result().ok().setData(Document.to_jsons(documents)).json_ret()

    @blue.route('/class/<int:cid>', methods=['GET'])
    @auth.login_required
    def GetClassRoute(cid: int):
        """ classId 查询文档 """
        documents = DocumentDao().queryDocumentsByClassId(uid=g.user, cid=cid)
        return Result().ok().setData(Document.to_jsons(documents)).json_ret()

    @blue.route('/<int:did>', methods=['GET'])
    @auth.login_required
    def GetOneRoute(did: int):
        """ did 查询文档 """
        document = DocumentDao().queryDocumentById(uid=g.user, did=did)
        if not document:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Not Found").json_ret()
        return Result.ok().setData(document.to_json()).json_ret()

    #######################################################################################################################

    @blue.route('/', methods=['POST'])
    @auth.login_required
    def InsertRoute():
        """ 插入文档 (DB + FS) """
        try:
            upload_file = request.files.get('file')
            # req_filename = request.form['filename']
            req_docClass = int(request.form['doc_class_id'])
            # if not (upload_file and req_filename and req_docClass):
            if not (upload_file and req_docClass):
                raise ParamError(ParamType.FORM)
        except:
            raise ParamError(ParamType.FORM)

        # Save
        server_filepath = f'{Config.UPLOAD_DOC_FOLDER}/{g.user}/'
        server_filename, type_ok, save_ok = FileUtil.saveFile(file=upload_file, path=server_filepath, file_image=False)
        if not type_ok:  # 格式错误
            return Result.error(ResultCode.BAD_REQUEST).setMessage('File Extension Error').json_ret()
        if not save_ok:  # 保存失败
            return Result.error(ResultCode.SAVE_FILE_FAILED).setMessage('Save Document Failed').json_ret()

        # Database
        filename = secure_filename(upload_file.filename)
        document = Document(did=-1, filename=filename, uuid=server_filename, docClass=req_docClass)
        status, new_document = DocumentDao().insertDocument(uid=g.user, document=document)
        if status == DbStatusType.FOUNDED:  # -1 永远不会
            os.remove(os.path.join(server_filepath, server_filename))
            return Result.error(ResultCode.HAS_EXISTED).setMessage("Document Existed").json_ret()
        elif status == DbStatusType.FAILED or not new_document:
            os.remove(os.path.join(server_filepath, server_filename))
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Document Insert Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_document.to_json()).json_ret()

    @blue.route('/', methods=['PUT'])
    @auth.login_required
    def UpdateRoute():
        """ 更新文档 (DB) """
        try:
            req_id = int(request.form['id'])
            req_filename = request.form['filename']
            req_docClass = int(request.form['doc_class_id'])
            if not req_filename or not (FileUtil.is_document(req_filename) or FileUtil.is_image(req_filename)):
                raise ParamError(ParamType.FORM)
        except:
            raise ParamError(ParamType.FORM)
        req_doc = Document(did=req_id, filename=req_filename, docClass=req_docClass)

        status, new_document = DocumentDao().updateDocument(uid=g.user, document=req_doc)
        if status == DbStatusType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Not Found").json_ret()
        elif status == DbStatusType.FAILED:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Document Update Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_document.to_json()).json_ret()

    @blue.route('/<int:did>', methods=['DELETE'])
    @auth.login_required
    def DeleteRoute(did: int):
        """ 删除文档 (DB + FS) """
        document: Document = DocumentDao().queryDocumentById(uid=g.user, did=did)
        status = DocumentDao().deleteDocument(uid=g.user, did=did)
        if status == DbStatusType.NOT_FOUND or not document:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Not Found").json_ret()
        elif status == DbStatusType.FAILED:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Document Delete Failed").json_ret()
        else:  # Success
            server_filepath = f'{Config.UPLOAD_DOC_FOLDER}/{g.user}/{document.uuid}'
            if os.path.exists(server_filepath):
                os.remove(server_filepath)
            return Result.ok().setData(document.to_json()).json_ret()


"""

Blue:

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
        
        fileClass = FileClassCtrl.getOneFileClass(usernameShared, DocClass(0, foldernameShared))
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


"""

"""

Ctrl:

def saveFile(file, username: str):
    '''
    保存用户文件
    '''
    if file:
        filepath = './usr/file/{}/'.format(username)  # 存放文件夹
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        filepath = os.path.join(filepath, file.filename)  # 最终路径
        file.save(filepath)
        if os.path.exists(filepath):
            return (file.filename, filepath)
        else:
            raise FileUploadError(file.filename)
    else:
        raise FileUploadError()


def getFile(username: str, filename: str):
    '''
    获得用户文件
    '''
    filepath = './usr/file/{}/'.format(username)
    filepath = os.path.join(filepath, filename)

    if not os.path.exists(filepath):
        raise FileNotExistError(filename)

    with open(filepath, 'rb') as f:
        return f
        
        
def addShareCode(usr: str, folder: str) -> bool:
    '''
    存储share code
    '''
    shareCodeDao = ShareCodeDao()
    return shareCodeDao.addShareCode(usr, folder)

def checkShareCode(usr: str, folder: str) -> bool:
    '''
    检查share code
    '''
    shareCodeDao = ShareCodeDao()
    return shareCodeDao.checkShareCode(usr, folder)
        

"""
