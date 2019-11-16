import json
import os
from typing import List

from flask import Blueprint, request, g
from flask_httpauth import HTTPTokenAuth

from app.model.dto.RawResult import RawResult
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.route.ParamType import ParamError, ParamType
from app.util import FileUtil


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/raw`
    """

    @auth.login_required
    @blue.route('/image', methods=['POST'])
    def UploadImageRoute():
        """ 上传图片 """
        try:
            upload_image = request.files.get('image')
            upload_type = request.form['type']
            if not upload_image:
                raise ParamError(ParamType.FORM)
        except:
            raise ParamError(ParamType.FORM)

        if upload_type == 'note':  # 笔记图片
            filepath = f'./usr/image/{g.user}/'
            filename, type_ok, save_ok = FileUtil.saveFile(file=upload_image, path=filepath, file_image=True)
            if not type_ok:  # 格式错误
                return Result.error(ResultCode.BAD_REQUEST).setMessage('Upload File Type Error').json_ret()
            if not save_ok:  # 保存失败
                return Result.error().setMessage('Image Save Failed').json_ret()
            else:  # 保存成功，返回路径
                return Result.ok().putData('filename', filename)  # 201911160411418089.jpg
        else:  # 其他格式
            return Result.error(ResultCode.BAD_REQUEST).setMessage('Not Support Request Upload Type').json_ret()

    @blue.route('/image/<int:uid>/<string:filename>', methods=['GET'])
    def GetImageRoute(uid: int, filename: str):
        """ 获取图片 (无需 Auth) """
        filepath = os.path.join(f'./usr/img/{uid}', filename)
        if not os.path.exists(filepath):
            return Result.error(ResultCode.NOT_FOUND).setMessage('Image Not Found').json_ret()
        else:
            with open(filepath, 'rb') as f:
                file_bytes = f.read()
            return RawResult.ok().setData(file_bytes).raw_ret(is_image=True)

    @auth.login_required
    @blue.route('/image', methods=['DELETE'])
    def DeleteImageRoute():
        """ 删除图片 """
        try:
            rawJson = json.loads(request.get_data(as_text=True))
            if not isinstance(rawJson, dict):
                raise ParamError(ParamType.RAW)
            request_type: str = rawJson['type']
            request_urls: List[str] = rawJson['urls']
            for url in request_urls:
                if not isinstance(url, str):
                    raise ParamError(ParamType.RAW)
        except:
            raise ParamError(ParamType.RAW)

        if request_type == 'note':  # 笔记图片
            count = 0
            for delUrl in rawJson:  # 直接存着图片地址
                filepath = f'./usr/img/{g.user}/{delUrl}'
                if os.path.exists(filepath):
                    os.remove(filepath)
                    count += 1 if not os.path.exists(filepath) else 0
            return Result.ok().putData('count', count).json_ret()

        else:  # 其他图片
            return Result.error(ResultCode.BAD_REQUEST).setMessage('Not Support Request Upload Type').json_ret()

    @auth.login_required
    @blue.route('/blob', methods=['GET'])
    def GetFileRoute():
        """ 获取文件 """
        # TODO ShareCode
        pass
