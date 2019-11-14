import json

from flask import Blueprint, request, g
from flask_httpauth import HTTPTokenAuth

from app.database.DbErrorType import DbErrorType
from app.database.dao.GroupDao import GroupDao
from app.model.po.Group import Group
from app.model.vo.Result import Result
from app.model.vo.ResultCode import ResultCode


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
        groups = GroupDao().queryAllGroups(g.username)
        return Result.ok().setData(Group.to_jsons(groups)).json_ret()

    @auth.login_required
    @blue.route("/<int:gid>", methods=['GET'])
    def GetByIdRoute(gid: int):
        """
        分组 id 查询
        """
        group = GroupDao().queryGroupById(g.username, gid)
        if not group:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        return Result.ok().setData(group.to_json()).json_ret()

    @auth.login_required
    @blue.route("/<string:name>", methods=['GET'])
    def GetByNameRoute(name: str):
        """
        分组名查询
        """
        group = GroupDao().queryGroupByName(g.username, name)
        if not group:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        return Result.ok().setData(group.to_json()).json_ret()

    @auth.login_required
    @blue.route("/default", methods=['GET'])
    def GetDefaultRoute():
        """
        默认分组
        """
        return Result.ok().setData(GroupDao().queryDefaultGroup(g.username).to_json()).json_ret()

    @auth.login_required
    @blue.route("/", methods=['POST'])
    def InsertGroup():
        """
        插入分组
        """
        rawJson = json.loads(request.get_data(as_text=True))
        group = Group.from_json(rawJson)
        ret = GroupDao().insertGroup(g.username, group)
        if ret == DbErrorType.FOUNDED:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Existed").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Group Insert Failed").json_ret()
        else:  # Success
            return Result.ok().setData(group.to_json()).json_ret()

    @auth.login_required
    @blue.route("/", methods=['PUT'])
    def UpdateRoute():
        """
        更新分组
        """
        rawJson = json.loads(request.get_data(as_text=True))
        group = Group.from_json(rawJson)
        ret = GroupDao().updateGroup(g.username, group)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Group Update Failed").json_ret()
        else:  # Success
            return Result.ok().setData(group.to_json()).json_ret()

    @auth.login_required
    @blue.route("/<int:gid>", methods=['DELETE'])
    def UpdateRoute(gid: int):
        """
        删除分组
        """
        rawJson = json.loads(request.get_data(as_text=True))
        group = Group.from_json(rawJson)
        ret = GroupDao().deleteGroup(g.username, gid)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Group Delete Failed").json_ret()
        else:  # Success
            return Result.ok().setData(group.to_json()).json_ret()
