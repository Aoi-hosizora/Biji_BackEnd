import io
import os
import random
import zipfile
from datetime import datetime
from typing import List

from flask import Blueprint, g, request, send_file, after_this_request
from flask_httpauth import HTTPTokenAuth
from app.config.Config import Config
from app.database.dao.DocumentDao import DocumentDao
from app.database.dao.ShareCodeDao import ShareCodeDao
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.model.po.Document import Document
from app.route.ParamType import ParamError, ParamType
from app.util import FileUtil


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/document/share`
    """

    @blue.route('/', methods=['GET'])
    @auth.login_required
    def GetUserShareCode():
        """ 获取用户所有共享码 getUserShareCodes """
        scs: List[str] = ShareCodeDao().getUserShareCodes(g.user)
        returns = []
        for sc in scs:
            dids = ShareCodeDao().getShareContent(sc)
            documents = DocumentDao().queryDocumentsByIds(g.user, dids)
            if len(documents) == 0:
                continue
            returns.append({
                'sc': sc,
                'documents': Document.to_jsons(documents)
            })
        return Result.ok().setData(returns).json_ret()

    @blue.route('/', methods=['POST'])
    @auth.login_required
    def NewShareCodeRoute():
        """ !!!! 新建共享码 addShareCode """
        try:
            req_Ex = int(request.form['ex'])
        except KeyError:
            req_Ex = Config.SHARE_TOKEN_EX
        except ValueError:
            raise ParamError(ParamType.FORM)

        cid = request.args.get('cid')
        if cid:  # 将整个集合共享 /share?cid
            try:
                cid = int(cid)
            except ValueError:
                raise ParamError(ParamType.FORM)
            documents = DocumentDao().queryDocumentsByClassId(g.user, int(cid))
            ids: List[int] = [did.id for did in documents]
        else:  # 文档集合分享 /share
            try:
                req_didList = request.form.getlist('did')
                if len(req_didList) == 0:
                    raise ParamError(ParamType.FORM)
                ids: List[int] = [int(did) for did in req_didList]
            except:
                raise ParamError(ParamType.FORM)
        # ids
        sc, docs = ShareCodeDao().addShareCode(uid=g.user, dids=ids, ex=req_Ex)
        if len(docs) == 0:
            return Result.error(ResultCode.SHARE_DOCUMENT_NULL).setMessage('Share Documents Null').json_ret()
        if sc == '':
            return Result.error(ResultCode.DATABASE_FAILED).setMessage('Document Share Code Generate Failed').json_ret()
        else:
            data = {
                'sc': sc,
                'documents': Document.to_jsons(docs)
            }
            return Result.ok().setData(data).json_ret()

    @blue.route('/', methods=['DELETE'])
    @auth.login_required
    def DeleteShareCodeRoute():
        """ 根据 共享码 (过滤) 删除 removeShareCodes """
        try:
            req_codes = request.form.getlist('sc')
        except:
            raise ParamError(ParamType.FORM)
        req_codes = list(filter(lambda code: code.startswith(ShareCodeDao.sc_prefix), req_codes))

        count = ShareCodeDao().removeShareCodes(g.user, req_codes)
        return Result.ok().putData('count', count).json_ret()

    @blue.route('/user', methods=['DELETE'])
    @auth.login_required
    def DeleteUserShareCodeRoute():
        """ 根据 用户 删除 removeUserShareCodes """
        count = ShareCodeDao().removeUserShareCodes(g.user)
        return Result.ok().putData('count', count).json_ret()

    #########################################################################################################################################################

    @blue.route('/<string:sc>', methods=['GET'])
    def GetRawDocument(sc: str):
        """ !!!! 通过 共享码 下载 """
        ok, uid, _ = ShareCodeDao.is_share_code(sc.strip(' \n\r\t'))
        if not ok:
            return Result.error(ResultCode.BAD_REQUEST).setMessage('Share Code Illegal').json_ret()

        dids = ShareCodeDao().getShareContent(sc)
        if len(dids) == 0:
            return Result.error(ResultCode.BAD_REQUEST).setMessage("Share Code Not Exist").json_ret()

        uuids: List[str] = DocumentDao().queryUuidByIds(uid, dids)

        if len(uuids) == 0:  # 没有文件
            return Result.error(ResultCode.SHARE_DOCUMENT_NULL).setMessage("Share Code Not Include File").json_ret()
        elif len(uuids) == 1:  # 单个文件
            filepath = os.path.join(f'{Config.UPLOAD_DOC_FOLDER}/{uid}', uuids[0])
            if not os.path.exists(filepath):
                return Result.error(ResultCode.NOT_FOUND).setMessage('File Not Found').json_ret()
            else:
                return send_file(filepath)

        else:  # 压缩文件
            filepaths = [os.path.join(f'{Config.UPLOAD_DOC_FOLDER}/{uid}', uuid) for uuid in uuids]
            existFilepaths = []  # 存在的文件
            for filepath in filepaths:
                if os.path.exists(filepath):
                    existFilepaths.append(filepath)

            time_uuid = datetime.now().strftime('%Y%m%d%H%M%S%f')
            zip_name = os.path.join(f'{Config.TEMP_SHARE_ZIP_FOLDER}', f'{time_uuid}.zip')

            # Not Exist & Create Zip
            while os.path.exists(zip_name):
                zip_name += random.randint(0, 9)
            if not FileUtil.createFile(zip_name):
                return Result.error().setMessage('Zip File Generate Failed').json_ret()

            @after_this_request
            def remove(response):
                # noinspection PyBroadException
                try:
                    os.remove(zip_name)
                except Exception as ex:
                    print(ex)
                    pass
                return response

            # noinspection PyBroadException
            try:
                with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
                    for filepath in existFilepaths:
                        z.write(filename=filepath, arcname=os.path.basename(filepath))
                with open(zip_name, 'rb') as f:
                    data = f.read()
                return send_file(io.BytesIO(data), mimetype='zip', attachment_filename=f'{sc}.zip')
            except Exception:
                return Result.error().setMessage('Zip File Generate Failed').json_ret()
