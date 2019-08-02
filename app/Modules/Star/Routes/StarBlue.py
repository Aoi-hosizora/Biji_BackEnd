from app.Utils import ErrorUtil, RespUtil

from app.Modules.Star.Controllers import StarCtrl
from app.Modules.Star.Models.StarItem import StarItem

from flask import Blueprint, request
from flask.app import Flask
import json

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
    username = RespUtil.getAuthUser(request.headers)
    stars = StarCtrl.getAllStars(username=username)
    return RespUtil.jsonRet(
        dict=StarItem.toJsonSet(stars), 
        code=ErrorUtil.Success
    )

@blue_Star.route("/insert", methods=['PUT'])
def InsertStarRoute():
    '''
    插入收藏路由处理 `POST /insert`

    @body `Star` JSON
    '''
    username = RespUtil.getAuthUser(request.headers)
    star = StarCtrl.getStarFromReqData(request.get_data(as_text=True))
    
    StarCtrl.insertStar(username=username, star=star)
    return RespUtil.jsonRet(
        dict=star.toJson(), 
        code=ErrorUtil.Success
    )

@blue_Star.route("/delete", methods=['DELETE'])
def DeleteStarRoute():
    '''
    删除收藏路由处理 `POST /delete`

    @body `Star` JSON
    '''
    username = RespUtil.getAuthUser(request.headers)
    star = StarCtrl.getStarFromReqData(request.get_data(as_text=True))

    StarCtrl.deleteStar(username=username, star=star)
    return RespUtil.jsonRet(
        dict=star.toJson(), 
        code=ErrorUtil.Success
    )