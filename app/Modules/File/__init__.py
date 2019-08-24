from flask.app import Flask

from app.Modules.File.Routes.FileBlue import register_blue_File
from app.Modules.File.Routes.FileClassBlue import register_blue_FileClass
from app.Modules.File.Routes.ErrorHandler import register_file_error_handler

def register_file_blue(app: Flask):
    '''
    注册 File 模块的蓝图
    '''
    register_blue_File(app)
    register_blue_FileClass(app)

def forward_file_error(error: TypeError):
    '''
    转发 File 模块的错误
    '''
    return register_file_error_handler(error)