import os

from flask import Blueprint, g, request
from flask_httpauth import HTTPTokenAuth

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
        """ 所有文档，只返回文件存在的记录 """
        documents = DocumentDao().queryAllDocuments(g.user)
        new_documents = []
        filepath = f'{Config.UPLOAD_DOC_FOLDER}/{g.user}/'
        for document in documents:
            if os.path.exists(filepath + document.uuid):  # 不删除不存在的记录
                new_documents.append(document)
        return Result().ok().setData(Document.to_jsons(new_documents)).json_ret()

    @blue.route('/class/<int:cid>', methods=['GET'])
    @auth.login_required
    def GetClassRoute(cid: int):
        """ classId 查询文档 """
        documents = DocumentDao().queryDocumentsByClassId(uid=g.user, cid=cid)
        new_documents = []
        filepath = f'{Config.UPLOAD_DOC_FOLDER}/{g.user}/'
        for document in documents:
            if os.path.exists(filepath + document.uuid):
                new_documents.append(document)
        return Result().ok().setData(Document.to_jsons(new_documents)).json_ret()

    @blue.route('/<int:did>', methods=['GET'])
    @auth.login_required
    def GetOneRoute(did: int):
        """ did 查询文档 """
        document = DocumentDao().queryDocumentById(uid=g.user, did=did)
        filepath = f'{Config.UPLOAD_DOC_FOLDER}/{g.user}/'
        if not document or not os.path.exists(filepath + document.uuid):
            return Result.error(ResultCode.NOT_FOUND).setMessage("Document Not Found").json_ret()
        return Result.ok().setData(document.to_json()).json_ret()

    #######################################################################################################################

    @blue.route('/', methods=['POST'])
    @auth.login_required
    def InsertRoute():
        """
        插入文档 (DB + FS)
        先保存文件，记录保存的文件名和 uuid (当前时间)
        然后将文件名 uuid classId 插入数据库，返回
        """
        try:
            upload_file = request.files.get('file')  # 包含文件名
            req_docClass = int(request.form['doc_class_id'])
            if not (upload_file and req_docClass):
                raise ParamError(ParamType.FORM)
        except:
            raise ParamError(ParamType.FORM)

        # # Save
        # file_len = len(upload_file.read())
        # if file_len > Config.MAX_UPLOAD_SIZE:  # 50M
        #     return Result.error(ResultCode.BAD_REQUEST).setMessage('File Out Of Size').json_ret()
        server_filepath = f'{Config.UPLOAD_DOC_FOLDER}/{g.user}/'
        uuid, type_ok, save_ok = FileUtil.saveFile(file=upload_file, path=server_filepath, file_image=False)
        if not type_ok:  # 格式错误
            return Result.error(ResultCode.BAD_REQUEST).setMessage('File Extension Error').json_ret()
        if not save_ok:  # 保存失败
            return Result.error(ResultCode.SAVE_FILE_FAILED).setMessage('Save Document Failed').json_ret()

        # Database
        document = Document(did=-1, filename=upload_file.filename, uuid=uuid, docClass=req_docClass)
        status, new_document = DocumentDao().insertDocument(uid=g.user, document=document)
        if status == DbStatusType.FOUNDED:  # -1 永远不会
            os.remove(os.path.join(server_filepath, uuid))
            return Result.error(ResultCode.HAS_EXISTED).setMessage("Document Existed").json_ret()
        elif status == DbStatusType.FAILED or not new_document:
            os.remove(os.path.join(server_filepath, uuid))
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Document Insert Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_document.to_json()).json_ret()

    @blue.route('/', methods=['PUT'])
    @auth.login_required
    def UpdateRoute():
        """
        更新文档 (DB)
        会更新文档分组和文件名
        """
        try:
            req_id = int(request.form['id'])
            req_filename = request.form['filename']
            req_docClass = int(request.form['doc_class_id'])
            if not req_filename or not (FileUtil.is_document(req_filename) or FileUtil.is_image(req_filename)):
                raise ParamError(ParamType.FORM)
        except:
            raise ParamError(ParamType.FORM)
        req_doc = Document(did=req_id, filename=req_filename, docClass=req_docClass)

        filepath = f'{Config.UPLOAD_DOC_FOLDER}/{g.user}/'
        status, new_document = DocumentDao().updateDocument(uid=g.user, document=req_doc)
        if status == DbStatusType.NOT_FOUND or not new_document or not os.path.exists(filepath + new_document.uuid):
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
