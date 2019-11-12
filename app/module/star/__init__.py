from flask.app import Flask

from app.module.star.Routes.StarBlue import register_blue_Star
from app.module.star.Routes.ErrorHandler import register_star_error_handler

def register_star_blue(app: Flask):
    '''
    注册 Star 模块的蓝图
    '''
    register_blue_Star(app)

def forward_star_error(error: TypeError):
    '''
    转发 Star 模块的错误
    '''
    return register_star_error_handler(error)