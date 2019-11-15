import json

from flask import Blueprint, request, g
from flask_httpauth import HTTPTokenAuth

from app.database.DbErrorType import DbErrorType
from app.database.dao.GroupDao import GroupDao
from app.model.po.Group import Group
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/group`
    """

    @auth.login_required
    @blue.route("/", methods=['GET'])
    def GetAllRoute():
        """
        所有分组
        """
        groups = GroupDao().queryAllGroups(uid=g.user)
        return Result.ok().setData(Group.to_jsons(groups)).json_ret()

    @auth.login_required
    @blue.route("/<int:gid>", methods=['GET'])
    def GetByIdRoute(gid: int):
        """
        gid 查询分组
        """
        group = GroupDao().queryGroupById(uid=g.user, gid=gid)
        if not group:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        return Result.ok().setData(group.to_json()).json_ret()

    @auth.login_required
    @blue.route("/<string:name>", methods=['GET'])
    def GetByNameRoute(name: str):
        """
        name 查询分组
        """
        group = GroupDao().queryGroupByName(uid=g.user, name=name)
        if not group:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        return Result.ok().setData(group.to_json()).json_ret()

    @auth.login_required
    @blue.route("/default", methods=['GET'])
    def GetDefaultRoute():
        """
        默认分组
        """
        return Result.ok().setData(
            GroupDao().queryDefaultGroup(uid=g.user).to_json()
        ).json_ret()

    @auth.login_required
    @blue.route("/", methods=['POST'])
    def InsertRoute():
        """
        插入
        """
        rawJson = json.loads(request.get_data(as_text=True))
        group = Group.from_json(rawJson)
        ret = GroupDao().insertGroup(uid=g.user, group=group)
        if ret == DbErrorType.FOUNDED:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Existed").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Group Insert Failed").json_ret()
        elif ret == DbErrorType.DUPLICATE:
            return Result.error().setMessage("Group Name Duplicate").json_ret()
        else:  # Success
            return Result.ok().setData(group.to_json()).json_ret()

    @auth.login_required
    @blue.route("/", methods=['PUT'])
    def UpdateRoute():
        """
        更新
        """
        rawJson = json.loads(request.get_data(as_text=True))
        group = Group.from_json(rawJson)
        ret = GroupDao().updateGroup(uid=g.user, group=group)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Group Update Failed").json_ret()
        elif ret == DbErrorType.DUPLICATE:
            return Result.error().setMessage("Group Name Duplicate").json_ret()
        elif ret == DbErrorType.DEFAULT:
            return Result.error().setMessage("Could Not Update Default Group").json_ret()
        else:  # Success
            return Result.ok().setData(group.to_json()).json_ret()

    @auth.login_required
    @blue.route("/<int:gid>", methods=['DELETE'])
    def DeleteRoute(gid: int):
        """
        删除
        """
        rawJson = json.loads(request.get_data(as_text=True))
        group = Group.from_json(rawJson)
        ret = GroupDao().deleteGroup(uid=g.user, gid=gid)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Group Delete Failed").json_ret()
        elif ret == DbErrorType.DEFAULT:
            return Result.error().setMessage("Could Not Delete Default Group").json_ret()
        else:  # Success
            return Result.ok().setData(group.to_json()).json_ret()
