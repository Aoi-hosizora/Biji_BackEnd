from app.util import ErrorUtil, RespUtil
from app.model.dto.Message import Message

from app.controller.schedule.Controllers import ScheduleCtrl
from app.model.po.Schedule import Schedule

from flask import Blueprint, request
from flask.app import Flask

import json


blue_Schedule = Blueprint("blue_Schedule", __name__, url_prefix="/schedule")

def register_blue_Schedule(app: Flask):
    app.register_blueprint(blue_Schedule)


@blue_Schedule.route("/download", methods=['GET'])
def DownloadScheduleRoute():
    '''
    下载课表路由处理 `GET /download`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)

    schedule = ScheduleCtrl.getSchedule(username=username)

    return RespUtil.jsonRet(
        data=schedule.toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Schedule.route("/upload", methods=['POST'])
def UploadScheduleRoute():
    '''
    上传课表路由处理 `POST /upload`
    '''
    print('UploadScheduleRoute ', request.get_data(as_text=True))
    username, newToken = RespUtil.getAuthUser(request.headers)
    form = json.loads(request.get_data(as_text=True))
    schedulejson = json.dumps(form['schedulejson'], ensure_ascii=False)
    schedule = Schedule(username, schedulejson)
    if ScheduleCtrl.getSchedule(username) is None:
        ScheduleCtrl.insertSchedule(schedule)
    else:
        ScheduleCtrl.updateSchedule(schedule=schedule)
    return RespUtil.jsonRet(
        data=Message(
            message="Schedule upload success",
        ).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Schedule.route("/delete", methods=['DELETE'])
def DeleteScheduleRoute():
    '''
    删除课表路由处理 `DELETE /delete`
    '''
    username, newToken = RespUtil.getAuthUser(request.headers)

    ScheduleCtrl.deleteSchedule(Schedule(username, ''))
    return RespUtil.jsonRet(
        data=Message(
            message="Schedule delete success",
        ).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Schedule.route("/update", methods=['PUT'])
def UpdateScheduleRoute ():
    '''
    更新用户课表 'PUT /update'
    :return:
    '''
    print('UpdateScheduleRoute ', request.get_data(as_text=True))
    username, newToken = RespUtil.getAuthUser(request.headers)
    form = json.loads(request.get_data(as_text=True))
    schedulejson = json.dumps(form['schedulejson'], ensure_ascii=False)
    schedule = Schedule(username, schedulejson)
    if ScheduleCtrl.getSchedule(username) is None:
        ScheduleCtrl.insertSchedule(schedule)
    else:
        ScheduleCtrl.updateSchedule(schedule=schedule)
    return RespUtil.jsonRet(
        data=Message(
            message="Schedule update success",
        ).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )

@blue_Schedule.route("/push", methods=['POST'])
def PushScheduleRoute():
    '''
    更新服务器用户课表 'POST /push'
    :return:
    '''
    print('PushScheduleRoute ', request.get_data(as_text=True))
    username, newToken = RespUtil.getAuthUser(request.headers)
    form = json.loads(request.get_data(as_text=True))
    schedulejson = json.dumps(form['schedulejson'], ensure_ascii=False)
    schedule = Schedule(username, schedulejson)
    if ScheduleCtrl.getSchedule(username) is None:
        ScheduleCtrl.insertSchedule(schedule)
    else:
        ScheduleCtrl.updateSchedule(schedule=schedule)
    return RespUtil.jsonRet(
        data=Message(
            message="Schedule update success",
        ).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )