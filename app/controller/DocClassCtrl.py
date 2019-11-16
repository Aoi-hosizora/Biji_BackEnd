from flask import Blueprint, g, request
from flask_httpauth import HTTPTokenAuth

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.dao.DocClassDao import DocClassDao
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.model.po.DocClass import DocClass
from app.route.ParamType import ParamError, ParamType


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/docclass`
    """

    @auth.login_required
    @blue.route('/', methods=['GET'])
    def GetAllRoute():
        """ 所有文件分组 """
        docClasses = DocClassDao().queryAllDocClasses(uid=g.user)
        return Result.ok().setData(DocClass.to_jsons(docClasses)).json_ret()

    @auth.login_required
    @blue.route('/<int:cid>', methods=['GET'])
    def GetByIdRoute(cid: int):
        """ id 获取文件分组 """
        docClass = DocClassDao().queryDocClassByIdOrName(uid=g.user, cid_name=int(cid))
        if not docClass:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Class Not Found").json_ret()
        return Result.ok().setData(docClass.to_json()).json_ret()

    @auth.login_required
    @blue.route('/', methods=['GET'])
    def GetByNameRoute():
        """ name 获取文件分组 """
        name = request.args.get('name')
        if not name:
            raise ParamError(ParamType.QUERY)
        docClass = DocClassDao().queryDocClassByIdOrName(uid=g.user, cid_name=str(name))
        if not docClass:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Class Not Found").json_ret()
        return Result.ok().setData(docClass.to_json()).json_ret()

    @auth.login_required
    @blue.route("/default", methods=['GET'])
    def GetDefaultRoute():
        """ 默认分组 """
        return Result.ok().setData(
            DocClassDao().queryDefaultDocClass(uid=g.user).to_json()
        ).json_ret()

    #######################################################################################################################

    @auth.login_required
    @blue.route('/', methods=['POST'])
    def InsertRoute():
        """ 新建文件分组 """
        try:
            req_name = request.form['name']
        except:
            raise ParamError(ParamType.FORM)
        if not (Config.FMT_DOCCLASS_NAME_MIN <= len(req_name) <= Config.FMT_DOCCLASS_NAME_MAX):
            return Result().error(ResultCode.BAD_REQUEST).setMessage('Format Error').json_ret()
        req_docclass = DocClass(cid=-1, name=req_name)

        status, new_docClass = DocClassDao().insertDocClass(uid=g.user, docClass=req_docclass)
        if status == DbStatusType.FOUNDED:
            return Result.error(ResultCode.HAS_EXISTED).setMessage("Document Class Existed").json_ret()
        elif status == DbStatusType.DUPLICATE:
            return Result.error(ResultCode.DUPLICATE_DEFAULT).setMessage("Document Class Name Duplicate").json_ret()
        elif status == DbStatusType.FAILED or not new_docClass:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Document Class Insert Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_docClass.to_json()).json_ret()

    @auth.login_required
    @blue.route('/', methods=['PUT'])
    def UpdateRoute():
        """ 更新文件分组 """
        try:
            req_id = int(request.form['id'])
            req_name = request.form['name']
        except:
            raise ParamError(ParamType.FORM)
        if not (Config.FMT_DOCCLASS_NAME_MIN <= len(req_name) <= Config.FMT_DOCCLASS_NAME_MAX):
            return Result().error(ResultCode.BAD_REQUEST).setMessage('Format Error').json_ret()
        req_docclass = DocClass(cid=req_id, name=req_name)

        status, new_docclass = DocClassDao().updateDocClass(uid=g.user, docClass=req_docclass)
        if status == DbStatusType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Class Not Found").json_ret()
        elif status == DbStatusType.DUPLICATE:
            return Result.error(ResultCode.DUPLICATE_DEFAULT).setMessage("Document Class Name Duplicate").json_ret()
        elif status == DbStatusType.DEFAULT:
            return Result.error(ResultCode.DUPLICATE_DEFAULT).setMessage("Could Not Update Default Document Class").json_ret()
        elif status == DbStatusType.FAILED:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Document Class Update Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_docclass.to_json()).json_ret()

    @auth.login_required
    @blue.route('/<int:cid>', methods=['DELETE'])
    def DeleteRoute(cid: int):
        """ 删除文件分组 """
        docclass = DocClassDao().queryDocClassByIdOrName(uid=g.user, cid_name=int(cid))
        status = DocClassDao().deleteDocClass(uid=g.user, cid=cid)
        if status == DbStatusType.NOT_FOUND or not docclass:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Class Not Found").json_ret()
        elif status == DbStatusType.DEFAULT:
            return Result.error(ResultCode.DUPLICATE_DEFAULT).setMessage("Could Not Delete Default Document Class").json_ret()
        elif status == DbStatusType.FAILED:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Document Class Delete Failed").json_ret()
        else:  # Success
            return Result.ok().setData(docclass.to_json()).json_ret()

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
