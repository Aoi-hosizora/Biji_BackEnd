from flask.app import Flask

from app.module.auth.Routes.RegLogBlue import register_blue_RegLog
from app.module.auth.Routes.ErrorHandler import register_auth_error_handler

def register_auth_blue(app: Flask):
    '''
    注册 Auth 模块的蓝图
    '''
    register_blue_RegLog(app)

def forward_auth_error(error: TypeError):
    '''
    转发 Auth 模块的错误
    '''
    return register_auth_error_handler(error)