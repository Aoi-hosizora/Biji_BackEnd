from app.Utils import ErrorUtil, RespUtil
from app.Models.Message import Message

from app.Modules.Note.Controllers import ImgCtrl 
from app.Modules.Note.Models.DelImg import DelImg

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
    username, newToken = RespUtil.getAuthUser(request.headers)
    img = request.files.get('noteimg')
    filepath = ImgCtrl.saveUserImg(username, img) # ./usr/img/aoihosizora/2019080919590813.jpg

    filepath = "%s/%s" % (filepath.split("/")[-2], filepath.split("/")[-1]) # aoihosizora/2019080919590813.jpg
    return RespUtil.jsonRet(
        dict=Message(
            message="Image upload success",
            detail=filepath
        ).toJson(), 
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_Img.route("/blob/<string:usr>/<string:img>", methods=["GET"])
def GetImgRoute(usr: str, img: str):
    '''
    查看图片路由处理 `GET /blob/<usr>/<img>`
    (不进行验证)
    '''
    image = ImgCtrl.getUserImg(usr, img)
    return RespUtil.jsonRet(
        isImg=True,
        dict=image,
        code=ErrorUtil.Success,
        headers={ 'Content-Type': 'image/png' }
    )

@blue_Img.route("/delete", methods=["DELETE"])
def DelImgRoute():
    '''
    删除图片路由处理 `DELETE /delete`
    (进行验证)
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    delimgs = ImgCtrl.getImgsFromReqData(request.get_data(as_text=True))
    l = ImgCtrl.delUsrImgs(username, delimgs)
    return RespUtil.jsonRet(
        dict=Message(
            message="Images delete success",
            detail=l
        ).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )