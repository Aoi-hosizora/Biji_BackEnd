from app.util import ErrorUtil, RespUtil
from app.model.dto.Message import Message

from app.module.star.Controllers import StarCtrl
from app.model.po.StarItem import StarItem

from flask import Blueprint, request
from flask.app import Flask

blue_Star = Blueprint("blue_Star", __name__, url_prefix="/star")
def register_blue_Star(app: Flask):
    '''
    注册收藏蓝图 `/star`

    `GET /all`
    '''
    app.register_blueprint(blue_Star)

@blue_Star.route("/all", methods=['GET'])
def AllStarRoute():
    '''
    获得所有收藏路由处理 `GET /all`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    stars = StarCtrl.getAllStars(username=username)
    return RespUtil.jsonRet(
        data=StarItem.toJsonSet(stars),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_Star.route("/insert", methods=['PUT'])
def InsertStarRoute():
    '''
    插入收藏路由处理 `POST /insert`

    @body `Star` JSON
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    star = StarCtrl.getStarFromReqData(request.get_data(as_text=True))
    
    StarCtrl.insertStar(username=username, star=star)
    return RespUtil.jsonRet(
        data=star.to_json(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_Star.route("/delete", methods=['DELETE'])
def DeleteStarRoute():
    '''
    删除收藏路由处理 `POST /delete`

    @body `Star` JSON
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    star = StarCtrl.getStarFromReqData(request.get_data(as_text=True))

    StarCtrl.deleteStar(username=username, star=star)
    return RespUtil.jsonRet(
        data=star.to_json(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_Star.route("/push", methods=['POST'])
def PushStarRoute():
    '''
    同步收藏路由处理 `POST /push`

    @body `Star []` JSON
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)
    stars = StarCtrl.getStarsFromReqData(request.get_data(as_text=True))

    StarCtrl.pushStar(username, stars)
    return RespUtil.jsonRet(
        data=Message(message="Stars push finished", detail=len(stars)).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )