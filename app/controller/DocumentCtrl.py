import json

from flask import Blueprint, g, request
from flask_httpauth import HTTPTokenAuth

from app.database.DbErrorType import DbErrorType
from app.database.dao.DocumentDao import DocumentDao
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.model.po.Document import Document


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/document`
    """

    @auth.login_required
    @blue.route('/', methods=['GET'])
    def GetAllRoute():
        """ 所有文件 """
        documents = DocumentDao().queryAllDocuments(g.user)
        return Result().ok().setData(Document.to_jsons(documents)).json_ret()

    @auth.login_required
    @blue.route('/<int:cid>', methods=['GET'])
    def GetClassRoute(cid: int):
        """ classId 查询文件 """
        documents = DocumentDao().queryDocumentsByClassId(uid=g.user, cid=cid)
        return Result().ok().setData(Document.to_jsons(documents)).json_ret()

    @auth.login_required
    @blue.route('/<int:did>', methods=['GET'])
    def GetOneRoute(did: int):
        """ did 查询文件 """
        document = DocumentDao().queryDocumentById(uid=g.user, did=did)
        if not document:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Not Found").json_ret()
        return Result.ok().setData(document.to_json()).json_ret()

    #######################################################################################################################

    @auth.login_required
    @blue.route('/', methods=['POST'])
    def InsertRoute():
        """ 插入文件 """
        # TODO 文件操作 Raw??
        rawJson = json.loads(request.get_data(as_text=True))
        document = Document.from_json(rawJson)
        ret = DocumentDao().insertDocument(uid=g.user, document=document)
        if ret == DbErrorType.FOUNDED:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Existed").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Document Insert Failed").json_ret()
        else:  # Success
            return Result.ok().setData(document.to_json()).json_ret()

    @auth.login_required
    @blue.route('/', methods=['PUT'])
    def UpdateRoute():
        """ 更新文件 """
        # 文件名 文件类别
        # TODO 文件操作
        rawJson = json.loads(request.get_data(as_text=True))
        document = Document.from_json(rawJson)
        ret = DocumentDao().updateDocument(uid=g.user, document=document)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Document Update Failed").json_ret()
        else:  # Success
            return Result.ok().setData(document.to_json()).json_ret()

    @auth.login_required
    @blue.route('/<int:did>', methods=['DELETE'])
    def DeleteRoute(did: int):
        """ 删除文件 """
        # TODO 文件操作
        ret = DocumentDao().deleteDocument(uid=g.user, did=did)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Document Delete Failed").json_ret()
        else:  # Success
            return Result.ok().json_ret()


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
        
        fileClass = FileClassCtrl.getOneFileClass(usernameShared, DocumentClass(0, foldernameShared))
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
