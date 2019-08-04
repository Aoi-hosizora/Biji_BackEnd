from app.Utils import ErrorUtil, RespUtil
from app.Models.Message import Message

from app.Modules.Schedule.Controllers import ScheduleCtrl
from app.Modules.Schedule.Models.Schedule import Schedule

from flask import Blueprint, request
from flask.app import Flask


blue_Schedule = Blueprint("blue_Schedule", __name__, url_prefix="/schedule")

def register_blue_Schedule(app: Flask):
    app.register_blueprint(blue_Schedule)


@blue_Schedule.route("/download", methods=['GET'])
def DownloadScheduleRoute():
    '''
    下载课表路由处理 `GET /download`
    '''
    username = RespUtil.getAuthUser(request.headers)

    schedule = ScheduleCtrl.getSchedule(username=username)

    return RespUtil.jsonRet(
        dict=schedule.toJson(),
        code=ErrorUtil.Success
    )


@blue_Schedule.route("/upload", methods=['POST'])
def UploadScheduleRoute():
    '''
    上传课表路由处理 `POST /upload`
    '''
    username = RespUtil.getAuthUser(request.headers)
    form = request.form
    schedulejson = form['schedulejson']
    schedule = Schedule(username, schedulejson)
    result = ScheduleCtrl.insertSchedule(schedule=schedule)
    return RespUtil.jsonRet(
        dict=Message(
            message="Schedule upload success",
        ).toJson(),
        code=ErrorUtil.Success
    )


@blue_Schedule.route("/delete", methods=['DELETE'])
def DeleteScheduleRoute():
    '''
    删除课表路由处理 `DELETE /delete`
    '''
    username = RespUtil.getAuthUser(request.headers)

    ScheduleCtrl.deleteSchedule(Schedule(username, ''))
    return RespUtil.jsonRet(
        dict=Message(
            message="Schedule delete success",
        ).toJson(),
        code=ErrorUtil.Success
    )


@blue_Schedule.route("/update", methods=['PUT'])
def UpdateScheduleRoute():
    '''
    更新用户课表 'PUT /update'
    :return:
    '''
    username = RespUtil.getAuthUser(request.headers)
    form = request.form
    schedulejson = form['schedulejson']
    schedule = Schedule(username, schedulejson)
    ScheduleCtrl.updateSchedule(schedule=schedule)
    return RespUtil.jsonRet(
        dict=Message(
            message="Schedule update success",
        ).toJson(),
        code=ErrorUtil.Success
    )
