from typing import List

from flask import Blueprint, request, g
from flask_httpauth import HTTPTokenAuth

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.dao.GroupDao import GroupDao
from app.model.po.Group import Group
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.route.ParamType import ParamError, ParamType


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/group`
    """

    @blue.route("/", methods=['GET'])
    @auth.login_required
    def GetAllRoute():
        """ 所有分组 / name """
        name = request.args.get('name')
        if name:  # 有查詢
            group = GroupDao().queryGroupByIdOrName(uid=g.user, gid_name=str(name))
            if not group:
                return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
            return Result.ok().setData(group.to_json()).json_ret()
        else:  # 無查詢
            groups = GroupDao().queryAllGroups(uid=g.user)
            return Result.ok().setData(Group.to_jsons(groups)).json_ret()

    @blue.route("/<int:gid>", methods=['GET'])
    @auth.login_required
    def GetByIdRoute(gid: int):
        """ gid 查询分组 """
        group = GroupDao().queryGroupByIdOrName(uid=g.user, gid_name=int(gid))
        if not group:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        return Result.ok().setData(group.to_json()).json_ret()

    @blue.route("/default", methods=['GET'])
    @auth.login_required
    def GetDefaultRoute():
        """ 默认分组 """
        return Result.ok().setData(
            GroupDao().queryDefaultGroup(uid=g.user).to_json()
        ).json_ret()

    #######################################################################################################################

    @blue.route("/", methods=['POST'])
    @auth.login_required
    def InsertRoute():
        """ 插入 """
        try:
            req_name = request.form['name']
            req_color = request.form.get('color')
        except:
            raise ParamError(ParamType.FORM)
        if not (Config.FMT_GROUP_NAME_MIN <= len(req_name) <= Config.FMT_GROUP_NAME_MAX):
            return Result().error(ResultCode.BAD_REQUEST).setMessage('Format Error').json_ret()
        req_group = Group(gid=-1, name=req_name, color=req_color)

        status, new_group = GroupDao().insertGroup(uid=g.user, group=req_group)
        if status == DbStatusType.FOUNDED:
            return Result.error(ResultCode.HAS_EXISTED).setMessage("Group Existed").json_ret()
        elif status == DbStatusType.DUPLICATE:
            return Result.error(ResultCode.DUPLICATE_FAILED).setMessage("Group Name Duplicate").json_ret()
        elif status == DbStatusType.FAILED or not new_group:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Group Insert Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_group.to_json()).json_ret()

    @blue.route("/", methods=['PUT'])
    @auth.login_required
    def UpdateRoute():
        """ 更新 """
        try:
            req_id = int(request.form['id'])
            req_name = request.form['name']
            req_order = int(request.form['order'])
            req_color = request.form['color']
        except:
            raise ParamError(ParamType.FORM)
        if not (Config.FMT_GROUP_NAME_MIN <= len(req_name) <= Config.FMT_GROUP_NAME_MAX):
            return Result().error(ResultCode.BAD_REQUEST).setMessage('Format Error').json_ret()
        req_group = Group(gid=req_id, name=req_name, order=req_order, color=req_color)

        status, new_group = GroupDao().updateGroup(uid=g.user, group=req_group)
        if status == DbStatusType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        elif status == DbStatusType.DUPLICATE:
            return Result.error(ResultCode.DUPLICATE_FAILED).setMessage("Group Name Duplicate").json_ret()
        elif status == DbStatusType.DEFAULT:
            return Result.error(ResultCode.DEFAULT_FAILED).setMessage("Could Not Update Default Group").json_ret()
        elif status == DbStatusType.FAILED or not new_group:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Group Update Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_group.to_json()).json_ret()

    # TODO 待測試
    @blue.route("/order", methods=['PUT'])
    @auth.login_required
    def UpdateOrderRoute():
        """ 更新顺序 """
        req_id_order = request.form.getlist('id_order')  # 3_4
        update_ids: List[int] = []
        update_orders: List[int] = []
        for id_order in req_id_order:
            try:
                id_order: [str] = id_order.split('_')
                update_ids.append(int(id_order[0]))
                update_orders.append(int(id_order[1]))
            except KeyError:
                pass

        status, count = GroupDao().updateGroupsOrder(uid=g.user, ids=update_ids, orders=update_orders)
        if status == DbStatusType.FAILED:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Group Update Failed").json_ret()
        else:  # Success
            return Result.ok().putData("count", count).json_ret()

    @blue.route("/<int:gid>", methods=['DELETE'])
    @auth.login_required
    def DeleteRoute(gid: int):
        """ 删除 """
        group: Group = GroupDao().queryGroupByIdOrName(uid=g.user, gid_name=int(gid))
        isToDefault: bool = request.args.get('default', 'false').lower() == 'true'

        status = GroupDao().deleteGroup(uid=g.user, gid=gid, toDefault=isToDefault)
        if status == DbStatusType.NOT_FOUND or not group:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        elif status == DbStatusType.DEFAULT:
            return Result.error(ResultCode.DEFAULT_FAILED).setMessage("Could Not Delete Default Group").json_ret()
        elif status == DbStatusType.FAILED:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Group Delete Failed").json_ret()
        else:  # Success
            return Result.ok().setData(group.to_json()).json_ret()
