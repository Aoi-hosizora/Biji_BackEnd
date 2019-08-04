from flask.app import Flask

from app.Modules.Log.Routes.LogBlue import register_blue_Log
from app.Modules.Log.Routes.ErrorHandler import register_log_error_handler

def register_log_blue(app: Flask):
    '''
    注册 Log 模块的蓝图
    '''
    register_blue_Log(app)

def forward_log_error(error: TypeError):
    '''
    转发 Log 模块的错误
    '''
    return register_log_error_handler(error)