from app.util import ErrorUtil, RespUtil
from app.model.dto.Message import Message
from app.route.exception.QueryError import QueryError

from app.controller.note.Controllers import GroupCtrl
from app.model.po.Group import Group

from flask import Blueprint, request
from flask.app import Flask

blue_Group = Blueprint("blue_Group", __name__, url_prefix="/group")


def register_blue_Group(app: Flask):
    """
    注册分组蓝图 `/group`

    `GET /all` `GET /one?id=<int>`
    `POST /update` `PUT /insert` `DELETE /delete`
    """
    app.register_blueprint(blue_Group)


@blue_Group.route("/all", methods=['GET'])
def AllGroupRoute():
    """
    获得所有分组路由处理 `GET /all`
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    groups = GroupCtrl.getAllGroups(username=username)
    return RespUtil.jsonRet(
        data=Group.toJsonSet(groups),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Group.route("/one", methods=['GET'])
def OneGroupRoute():
    """
    获得单个分组路由处理 `GET /one?id=<int>`
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    id = request.args.get('id')
    try:
        id = int(id)
    except:
        raise QueryError(list(['id']))

    groups = GroupCtrl.getOneGroup(username=username, id=id)
    return RespUtil.jsonRet(
        data=groups.to_json(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Group.route("/update", methods=['Post'])
def UpdateGroupRoute():
    """
    更新分组路由处理 `POST /update`

    @body `Group` JSON
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    group = GroupCtrl.getGroupFromReqData(request.get_data(as_text=True))

    GroupCtrl.updateGroup(username=username, group=group)
    return RespUtil.jsonRet(
        data=group.to_json(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Group.route("/insert", methods=['Put'])
def InsertGroupRoute():
    """
    插入分组路由处理 `POST /insert`

    @body `Group` JSON
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    group = GroupCtrl.getGroupFromReqData(request.get_data(as_text=True))

    GroupCtrl.insertGroup(username=username, group=group)
    return RespUtil.jsonRet(
        data=group.to_json(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Group.route("/delete", methods=['Delete'])
def DeleteGroupRoute():
    """
    删除分组路由处理 `POST /delete`

    @body `Group` JSON
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    group = GroupCtrl.getGroupFromReqData(request.get_data(as_text=True))

    GroupCtrl.deleteGroup(username=username, group=group)
    return RespUtil.jsonRet(
        data=group.to_json(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Group.route("/push", methods=['POST'])
def PushGroupRoute():
    """
    同步笔记路由处理 `POST /push`

    @body `Note []` JSON
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    groups = GroupCtrl.getGroupsFromReqData(request.get_data(as_text=True))

    GroupCtrl.pushGroup(username, groups)
    return RespUtil.jsonRet(
        data=Message(message="Groups push finished", detail=len(groups)).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )
