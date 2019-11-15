from flask import Blueprint, g, request
from flask_httpauth import HTTPTokenAuth

from app.database.DbErrorType import DbErrorType
from app.database.dao.ScheduleDao import ScheduleDao
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/schedule`
    """

    @auth.login_required
    @blue.route('/', methods=['GET'])
    def GetRoute():
        """
        获得 课程表
        """
        schedule_data: str = ScheduleDao().querySchedule(uid=g.user)
        if schedule_data == '':
            return Result.error(ResultCode.NOT_FOUND).setMessage('Get Schedule Null').json_ret()
        else:
            return Result.ok().setData(schedule_data).json_ret()

    @auth.login_required
    @blue.route('/', methods=['PUT'])
    def UpdateRoute():
        """
        更新/新建 课程表
        """
        schedule_data = request.get_data(as_text=True)
        ret = ScheduleDao().updateSchedule(uid=g.user, data=schedule_data)
        if ret == DbErrorType.FAILED:
            return Result.error(ResultCode.NOT_FOUND).setMessage('Update Schedule Failed').json_ret()
        else:
            return Result.ok().json_ret()

    @auth.login_required
    @blue.route('/', methods=['DELETE'])
    def DeleteRoute():
        """
        删除 课程表
        """
        ret = ScheduleDao().deleteSchedule(uid=g.user)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage('Delete Schedule Not Found').json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error(ResultCode.NOT_FOUND).setMessage('Delete Schedule Failed').json_ret()
        else:
            return Result.ok().json_ret()
