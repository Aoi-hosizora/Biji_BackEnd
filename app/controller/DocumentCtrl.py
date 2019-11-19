import os
import zipfile
from typing import List

from flask import Blueprint, g, request, send_file
from flask_httpauth import HTTPTokenAuth
from werkzeug.utils import secure_filename

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.dao.DocumentDao import DocumentDao
from app.database.dao.ShareCodeDao import ShareCodeDao
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

    @blue.route('/share', methods=['POST'])
    @auth.login_required
    def NewShareCodeRoute():
        """ 新建共享码 addShareCode """
        try:
            req_Ex = int(request.form['ex'])
        except ValueError:
            req_Ex = Config.SHARE_TOKEN_EX

        cid = request.args.get('cid')
        if cid and isinstance(cid, int):  # 将整个集合共享 /share?cid
            documents = DocumentDao().queryDocumentsByClassId(g.user, int(cid))
            ids: List[int] = [did.id for did in documents]
        else:  # /share
            try:
                req_didList = request.form.getlist('id')
                if len(req_didList) == 0:
                    raise ParamError(ParamType.FORM)
                ids: List[int] = [int(did) for did in req_didList]
            except:
                raise ParamError(ParamType.FORM)

        sc = ShareCodeDao().addShareCode(uid=g.user, dids=ids, ex=req_Ex)
        if sc == '':
            return Result.error(ResultCode.DATABASE_FAILED).setMessage('Document Share Code Generate Failed').json_ret()
        else:
            return Result.ok().putData('sc', sc).json_ret()

    @blue.route('/share', methods=['GET'])
    @auth.login_required
    def GetUserShareCode():
        """ 获取用户所有共享码 getUserShareCodes """
        scs: List[int] = ShareCodeDao().getUserShareCodes(g.user)
        return Result.ok().setData(scs).to_json()

    @blue.route('/share', methods=['DELETE'])
    @auth.login_required
    def DeleteShareCodeRoute():
        """ 根据 共享码 (过滤) 删除 removeShareCodes """
        try:
            req_codes = request.form.getlist('sc')
        except:
            raise ParamError(ParamType.FORM)
        req_codes = list(filter(lambda code: code.startswith(ShareCodeDao.sc_prefix), req_codes))

        count = ShareCodeDao().removeShareCodes(g.user, req_codes)
        return Result.ok().putData('count', count)

    @blue.route('/share/user', methods=['DELETE'])
    @auth.login_required
    def DeleteUserShareCodeRoute():
        """ 根据 用户 删除 removeUserShareCodes """
        count = ShareCodeDao().removeUserShareCodes(g.user)
        return Result.ok().putData('count', count)

    @blue.route('/share/<string:sc>', methods=['GET'])
    def GetRawDocument(sc: str):
        """ 通过 共享码 下载 """
        uid, dids = ShareCodeDao().getShareContent(sc)
        documents = DocumentDao().queryDocumentByIds(uid, dids)
        uuids = [doc.uuid for doc in documents]

        if len(uuids) == 1:  # 单个文件
            filepath = os.path.join(f'{Config.UPLOAD_DOC_FOLDER}/{uid}', uuids[0])
            if not os.path.exists(filepath):
                return Result.error(ResultCode.NOT_FOUND).setMessage('File Not Found').putData('filename', filepath).json_ret()
            else:
                return send_file(filepath)

        else:  # 压缩文件
            filepaths = [os.path.join(f'{Config.UPLOAD_DOC_FOLDER}/{uid}', uuid) for uuid in uuids]
            existFilepaths = []  # 存在的文件
            for filepath in filepaths:
                if os.path.exists(filepath):
                    existFilepaths.append(filepath)

            # noinspection PyBroadException
            try:
                with zipfile.ZipExtFile('tmp.zip', 'w', zipfile.ZIP_STORED) as zip:
                    for filepath in existFilepaths:
                        zip.write(filepath)
                    return send_file('tmp.file')
            except:
                return Result.error().setMessage('Zip File Generate Failed').json_ret()

