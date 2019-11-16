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
        schedule_data: str = ScheduleDao().querySchedule(uid=g.user)
        if schedule_data == '':
            return Result.error(ResultCode.NOT_FOUND).setMessage('Schedule Not Found').json_ret()
        else:
            return Result.ok().putData("schedule", schedule_data).json_ret()

    #######################################################################################################################

    @blue.route('/', methods=['PUT'])
    @auth.login_required
    def UpdateRoute():
        """ 更新/新建 课程表 """
        schedule_data = request.form.get('schedule')
        if not schedule_data:
            raise ParamError(ParamType.FORM)
        status = ScheduleDao().updateSchedule(uid=g.user, data=schedule_data)
        if status == DbStatusType.FAILED:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage('Update Schedule Failed').json_ret()
        else:
            return Result.ok().json_ret()

    @blue.route('/', methods=['DELETE'])
    @auth.login_required
    def DeleteRoute():
        """ 删除 课程表 """
        status = ScheduleDao().deleteSchedule(uid=g.user)
        if status == DbStatusType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage('Schedule Not Found').json_ret()
        elif status == DbStatusType.FAILED:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage('Delete Schedule Failed').json_ret()
        else:
            return Result.ok().json_ret()
