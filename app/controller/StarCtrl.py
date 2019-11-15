import json
from typing import List

from flask import Blueprint, request, g
from flask_httpauth import HTTPTokenAuth

from app.database.DbErrorType import DbErrorType
from app.database.dao.StarDao import StarDao
from app.model.po.StarItem import StarItem
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.route.ParamError import ParamError, ParamType


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/star`
    """

    @auth.login_required
    @blue.route("/", methods=['GET'])
    def GetAllRoute():
        """ 所有分组 """
        stars = StarDao().queryAllStars(uid=g.user)
        return Result.ok().setData(StarItem.to_jsons(stars)).json_ret()

    #######################################################################################################################

    @auth.login_required
    @blue.route("/", methods=['POST'])
    def InsertRoute():
        """ 插入 """
        rawJson = json.loads(request.get_data(as_text=True))
        star = StarItem.from_json(rawJson)
        ret = StarDao().insertStar(uid=g.user, star=star)
        if ret == DbErrorType.FOUNDED:
            return Result.error(ResultCode.NOT_FOUND).setMessage("StarItem Existed").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("StatItem Insert Failed").json_ret()
        elif ret == DbErrorType.DUPLICATE:
            return Result.error().setMessage("StatItem Url Duplicate").json_ret()
        else:  # Success
            return Result.ok().setData(star.to_json()).json_ret()

    @auth.login_required
    @blue.route("/<int:sid>", methods=['DELETE'])
    def DeleteRoute(sid: int):
        """ 删除 """
        ret = StarDao().deleteStar(uid=g.user, sid=sid)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("StarItem Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("StarItem Delete Failed").json_ret()
        else:  # Success
            return Result.ok().json_ret()

    @auth.login_required
    @blue.route("/delete/", methods=['DELETE'])
    def DeletesRoute():
        """ 删除多个 """
        rawJson: List[int] = json.loads(request.get_data(as_text=True))
        if not isinstance(rawJson, list):
            raise ParamError(ParamType.RAW)
        for item in rawJson:
            if not isinstance(item, int):
                raise ParamError(ParamType.RAW)

        ret = StarDao().deleteStars(uid=g.ussername, ids=rawJson)
        if ret == -1:
            return Result().error().json_ret()
        else:
            return Result().ok().putData("count", ret).json_ret()
