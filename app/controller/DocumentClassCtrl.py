import json

from flask import Blueprint, g, request
from flask_httpauth import HTTPTokenAuth

from app.database.DbErrorType import DbErrorType
from app.database.dao.DocumentClassDao import DocumentClassDao
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.model.po.DocumentClass import DocumentClass


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/document/class`
    """

    @auth.login_required
    @blue.route('/', methods=['GET'])
    def GetAllRoute():
        """ 所有文件分组 """
        docClasses = DocumentClassDao().queryAllDocumentClasses(uid=g.user)
        return Result.ok().setData(DocumentClass.to_jsons(docClasses)).json_ret()

    @auth.login_required
    @blue.route('/<int:cid>', methods=['GET'])
    def GetRoute(cid: int):
        """ id 获取文件分组 """
        docClass = DocumentClassDao().queryDocumentClassById(uid=g.user, cid=cid)
        if not docClass:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Class Not Found").json_ret()
        return Result.ok().setData(docClass.to_json()).json_ret()

    @auth.login_required
    @blue.route("/default", methods=['GET'])
    def GetDefaultRoute():
        """ 默认分组 """
        return Result.ok().setData(
            DocumentClassDao().queryDefaultDocumentClass(uid=g.user).to_json()
        ).json_ret()

    #######################################################################################################################

    @auth.login_required
    @blue.route('/', methods=['POST'])
    def InsertRoute():
        """ 新建文件分组 """
        rawJson = json.loads(request.get_data(as_text=True))
        docClass = DocumentClass.from_json(rawJson)
        ret = DocumentClassDao().insertDocumentClass(uid=g.user, docClass=docClass)
        if ret == DbErrorType.FOUNDED:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Class Existed").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Document Class Insert Failed").json_ret()
        elif ret == DbErrorType.DUPLICATE:
            return Result.error().setMessage("Document Class Name Duplicate").json_ret()
        else:  # Success
            return Result.ok().setData(docClass.to_json()).json_ret()

    @auth.login_required
    @blue.route('/', methods=['PUT'])
    def UpdateRoute():
        """ 更新文件分组 """
        rawJson = json.loads(request.get_data(as_text=True))
        docClass = DocumentClass.from_json(rawJson)
        ret = DocumentClassDao().updateDocumentClass(uid=g.user, docClass=docClass)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Class Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Document Class Update Failed").json_ret()
        elif ret == DbErrorType.DUPLICATE:
            return Result.error().setMessage("Document Class Name Duplicate").json_ret()
        elif ret == DbErrorType.DEFAULT:
            return Result.error().setMessage("Could Not Update Default Document Class").json_ret()
        else:  # Success
            return Result.ok().setData(docClass.to_json()).json_ret()

    @auth.login_required
    @blue.route('/<int:cid>', methods=['DELETE'])
    def DeleteRoute(cid: int):
        """ 删除文件分组 """
        ret = DocumentClassDao().deleteDocumentClass(uid=g.user, cid=cid)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Class Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Document Class Delete Failed").json_ret()
        elif ret == DbErrorType.DEFAULT:
            return Result.error().setMessage("Could Not Delete Default Document Class").json_ret()
        else:  # Success
            return Result.ok().json_ret()

    # @auth.login_required
    # @blue.route('/share', methods=['DELETE'])
    # def ShareRoute():
    #     """
    #     生成文件共享二维码
    #     """
    #     pass

    '''
    @blue_FileClass.route("/share", methods=['GET'])
    def ShareFilesRoute():
        username, newToken = RespUtil.getAuthUser(request.headers)
        foldername = request.args.get('foldername')
        codeJson = FileClassCtrl.shareCode2Json(username=username, foldername=foldername)
        shareCodeDao = ShareCodeDao()
        shareCodeDao.addShareCode(username+foldername, codeJson)
        qrcode.make(data=codeJson).save('temp.png')
        return send_file('temp.png')
        
    def shareCode2Json(username: str, foldername: str):
        return "{\"usr\":\""+username+"\",\"folder\":\""+foldername+"\"}"

    '''
