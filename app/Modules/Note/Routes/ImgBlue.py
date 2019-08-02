from app.Utils import ErrorUtil, RespUtil
from app.Models.Message import Message

from app.Modules.Note.Controllers import ImgCtrl 

from flask import Blueprint, request
from flask.app import Flask
import json

blue_Img = Blueprint("blue_Img", __name__, url_prefix="/note/img")
def register_blue_Img(app: Flask):
    '''
    注册笔记图片蓝图 `/note/img`

    `POST /upload` `GET /<usr>/<img>`
    '''
    app.register_blueprint(blue_Img)

@blue_Img.route("/upload", methods=["POST"])
def UploadImgRoute():
    '''
    上传笔记图片路由处理 `POST /upload`
    '''
    username = RespUtil.getAuthUser(request.headers)
    img = request.files.get('noteimg')
    filename = ImgCtrl.saveUserImg(username, img)
    return RespUtil.jsonRet(
        dict=Message(
            message="Image upload success",
            detail=filename
        ).toJson(), 
        code=ErrorUtil.Success
    )

@blue_Img.route("/blob/<string:usr>/<string:img>", methods=["GET"])
def GetImgRoute(usr: str, img: str):
    '''
    查看图片路由处理 `GET /blob/<usr>/<img>`
    '''
    username = RespUtil.getAuthUser(request.headers)
    image = ImgCtrl.getUserImg(usr, img)
    return RespUtil.jsonRet(
        isImg=True,
        dict=image,
        code=ErrorUtil.Success,
        headers={ 'Content-Type': 'image/png' },
    )