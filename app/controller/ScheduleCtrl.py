from flask import Blueprint, g, request
from flask_httpauth import HTTPTokenAuth

from app.database.DbStatusType import DbStatusType
from app.database.dao.ScheduleDao import ScheduleDao
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.route.ParamType import ParamError, ParamType


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/schedule`
    """

    @blue.route('/', methods=['GET'])
    @auth.login_required
    def GetRoute():
        """ 获得 课程表 """
        sc, week = ScheduleDao().querySchedule(uid=g.user)
        if not sc:
            return Result.error(ResultCode.NOT_FOUND).setMessage('Schedule Not Found').json_ret()
        else:
            return Result.ok().putData("schedule", sc).putData("week", week).json_ret()

    #######################################################################################################################

    @blue.route('/', methods=['PUT'])
    @auth.login_required
    def UpdateRoute():
        """ 更新/新建 课程表 """
        try:
            schedule_data = request.form.get('schedule')
            curr_week = int(request.form.get('week'))
        except (TypeError, ValueError):
            raise ParamError(ParamType.FORM)
        if not schedule_data:
            raise ParamError(ParamType.FORM)
        if curr_week <= 0:
            raise ParamError(ParamType.FORM)
        status, new_sc, new_week = ScheduleDao().updateSchedule(uid=g.user, data=schedule_data, week=curr_week)
        if status == DbStatusType.FAILED or not new_sc or new_week <= 0:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage('Update Schedule Failed').json_ret()
        else:
            return Result.ok().putData('schedule', new_sc).putData('week', new_week).json_ret()

    @blue.route('/', methods=['DELETE'])
    @auth.login_required
    def DeleteRoute():
        """ 删除 课程表 """
        status, schedule, week = ScheduleDao().deleteSchedule(uid=g.user)
        if status == DbStatusType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage('Schedule Not Found').json_ret()
        elif status == DbStatusType.FAILED:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage('Delete Schedule Failed').json_ret()
        else:
            return Result.ok().putData('schedule', schedule).putData('week', week).json_ret()
