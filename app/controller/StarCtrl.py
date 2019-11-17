from typing import List

from flask import Blueprint, request, g
from flask_httpauth import HTTPTokenAuth

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.dao.StarDao import StarDao
from app.model.po.StarItem import StarItem
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.route.ParamType import ParamError, ParamType


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/star`
    """

    @blue.route("/", methods=['GET'])
    @auth.login_required
    def GetAllRoute():
        """ 所有分组 """
        stars = StarDao().queryAllStars(uid=g.user)
        return Result.ok().setData(StarItem.to_jsons(stars)).json_ret()

    @blue.route("/<int:sid>", methods=['GET'])
    @auth.login_required
    def GetByIdRoute(sid: int):
        """ 根据 sid 获取分组 """
        star = StarDao().queryStarByIdOrUrl(uid=g.user, sid_url=sid)
        if not star:
            return Result.error(ResultCode.NOT_FOUND).setMessage("StarItem Not Found").json_ret()
        return Result.ok().setData(star.to_json()).json_ret()

    #######################################################################################################################

    @blue.route("/", methods=['POST'])
    @auth.login_required
    def InsertRoute():
        """ 插入 """
        try:
            req_title = request.form['title']
            req_url = request.form['url']
            req_content = request.form['content']

            if len(req_title) > Config.FMT_STAR_TITLE_MAX:
                req_title = req_title[:Config.FMT_STAR_TITLE_MAX - 3] + '...'
            if len(req_content) > Config.FMT_STAR_CONTENT_MAX:
                req_content = req_content[:Config.FMT_STAR_CONTENT_MAX - 3] + '...'
        except:
            raise ParamError(ParamType.FORM)
        req_star = StarItem(sid=-1, title=req_title, url=req_url, content=req_content)

        status, new_star = StarDao().insertStar(uid=g.user, star=req_star)
        if status == DbStatusType.FOUNDED:
            return Result.error(ResultCode.HAS_EXISTED).setMessage("StarItem Existed").json_ret()
        elif status == DbStatusType.DUPLICATE:
            return Result.error(ResultCode.DUPLICATE_DEFAULT).setMessage("StatItem Url Duplicate").json_ret()
        elif status == DbStatusType.FAILED or not new_star:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("StatItem Insert Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_star.to_json()).json_ret()

    @blue.route("/<int:sid>", methods=['DELETE'])
    @auth.login_required
    def DeleteRoute(sid: int):
        """ 删除 """
        starItem: StarItem = StarDao().queryStarByIdOrUrl(uid=g.user, sid_url=sid)
        count = StarDao().deleteStars(uid=g.user, ids=[sid])
        if count == 0 or not starItem:
            return Result().error(ResultCode.NOT_FOUND).setMessage("StarItem Not Found").json_ret()
        elif count == -1:
            return Result().error(ResultCode.DATABASE_FAILED).setMessage("StarItem Delete Failed").json_ret()
        else:
            return Result().ok().setData(starItem.to_json()).json_ret()

    @blue.route("/", methods=['DELETE'])
    @auth.login_required
    def DeletesRoute():
        """ 删除多个 """
        req_ids: List = request.form.getlist('id')
        delete_ids: List[int] = []
        for req_id in req_ids:
            try:
                delete_ids.append(int(req_id))
            except KeyError:
                pass
        count = StarDao().deleteStars(uid=g.user, ids=delete_ids)
        if count == -1:
            return Result().error(ResultCode.DATABASE_FAILED).setMessage("StarItem Delete Failed").json_ret()
        else:
            return Result().ok().putData("count", count).json_ret()
