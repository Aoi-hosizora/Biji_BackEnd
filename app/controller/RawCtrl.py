import os
from typing import List

from flask import Blueprint, request, g, send_file
from flask_httpauth import HTTPTokenAuth

from app.config.Config import Config
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.route.ParamType import ParamError, ParamType
from app.util import FileUtil


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/raw`
    """

    @blue.route('/image', methods=['POST'])
    @auth.login_required
    def UploadImageRoute():
        """ 上传图片 """
        try:
            req_image = request.files.get('image')
            req_type = request.form['type']
            if not req_image:
                raise ParamError(ParamType.FORM)
        except:
            raise ParamError(ParamType.FORM)

        if req_type == 'note':  # 笔记图片
            filepath = f'{Config.UPLOAD_IMAGE_FOLDER}/{g.user}/'
            filename, type_ok, save_ok = FileUtil.saveFile(file=req_image, path=filepath, file_image=True)
            if not type_ok:  # 格式错误
                return Result.error(ResultCode.BAD_REQUEST).setMessage('File Extension Error').json_ret()
            if not save_ok:  # 保存失败
                return Result.error(ResultCode.SAVE_FILE_FAILED).setMessage('Save Image Failed').json_ret()
            else:  # 保存成功，返回路径
                return Result.ok().putData('filename', filename).json_ret()  # 201911160411418089.jpg

        else:  # 其他类型图片
            return Result.error(ResultCode.BAD_REQUEST).setMessage('Not Support Upload Type').json_ret()

    @blue.route('/image', methods=['DELETE'])
    @auth.login_required
    def DeleteImageRoute():
        """ 删除图片 """
        try:
            req_type = request.form['type']
            req_urls: List = request.form.getlist('urls')
        except:
            raise ParamError(ParamType.FORM)

        if req_type == 'note':  # 笔记图片
            count = 0
            for delUrl in req_urls:  # 直接存着图片地址
                filepath = f'{Config.UPLOAD_IMAGE_FOLDER}/{g.user}/{delUrl}'
                if os.path.exists(filepath):
                    os.remove(filepath)
                    count += 1 if not os.path.exists(filepath) else 0
            return Result.ok().putData('count', count).json_ret()

        else:  # 其他类型图片
            return Result.error(ResultCode.BAD_REQUEST).setMessage('Not Support Upload Type').json_ret()

    #######################################################################################################################

    @blue.route('/image/<int:uid>/<string:filename>', methods=['GET'])
    def GetImageRoute(uid: int, filename: str):
        """ 获取图片 (无需 Auth) """
        filepath = os.path.join(f'{Config.UPLOAD_IMAGE_FOLDER}/{uid}', filename)
        if not os.path.exists(filepath):
            return Result.error(ResultCode.NOT_FOUND).setMessage('Image Not Found').json_ret()
        else:
            return send_file(filepath)
