import json

from flask import Blueprint, request, g
from flask_httpauth import HTTPTokenAuth

from app.database.DbErrorType import DbErrorType
from app.database.dao.StarDao import StarDao
from app.model.po.StarItem import StarItem
from app.model.vo.Result import Result
from app.model.vo.ResultCode import ResultCode
from app.route.ParamError import ParamError, ParamType


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/star`
    """

    @auth.login_required
    @blue.route("/", methods=['GET'])
    def GetAllRoute():
        """
        所有分组
        """
        stars = StarDao().queryAllStars(g.username)
        return Result.ok().setData(StarItem.to_jsons(stars)).json_ret()

    @auth.login_required
    @blue.route("/", methods=['POST'])
    def InsertRoute():
        """
        插入
        """
        rawJson = json.loads(request.get_data(as_text=True))
        star = StarItem.from_json(rawJson)
        ret = StarDao().insertStar(g.username, star)
        if ret == DbErrorType.FOUNDED:
            return Result.error(ResultCode.NOT_FOUND).setMessage("StarItem Existed").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("StatItem Insert Failed").json_ret()
        else:  # Success
            return Result.ok().setData(star.to_json()).json_ret()

    @auth.login_required
    @blue.route("/<int:sid>", methods=['DELETE'])
    def DeleteRoute(sid: int):
        """
        删除
        """
        rawJson = json.loads(request.get_data(as_text=True))
        star = StarItem.from_json(rawJson)
        ret = StarDao().deleteStar(g.username, sid)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("StarItem Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("StarItem Delete Failed").json_ret()
        else:  # Success
            return Result.ok().setData(star.to_json()).json_ret()

    @auth.login_required
    @blue.route("/delete/", methods=['DELETE'])
    def DeletesRoute():
        """
        删除所有
        """
        rawJson = json.loads(request.get_data(as_text=True))
        if not isinstance(rawJson, list):
            raise ParamError(ParamType.RAW)
        for item in rawJson:
            if not isinstance(item, int):
                raise ParamError(ParamType.RAW)

        ret = StarDao().deleteStars(g.ussername, rawJson)
        if ret == -1:
            return Result().error().json_ret()
        else:
            return Result().ok().putData("count", ret).json_ret()
