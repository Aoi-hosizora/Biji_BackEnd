from flask.app import Flask

from app.Modules.Schedule.Routes.ScheduleBlue import register_blue_Schedule
from app.Modules.Schedule.Routes.ErrorHandler import register_schedule_error_handler

def register_schedule_blue(app: Flask):
    '''
    注册 Schedule 模块的蓝图
    '''
    register_blue_Schedule(app)

def forward_schedule_error(error: TypeError):
    '''
    转发 Schedule 模块的错误
    '''
    return register_schedule_error_handler(error)