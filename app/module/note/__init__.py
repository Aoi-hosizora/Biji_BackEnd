from flask.app import Flask

from app.module.note.Routes.NoteBlue import register_blue_Note
from app.module.note.Routes.GroupBlue import register_blue_Group
from app.module.note.Routes.ImgBlue import register_blue_Img
from app.module.note.Routes.ErrorHandler import register_note_error_handler

def register_note_blue(app: Flask):
    '''
    注册 Note 模块的蓝图
    '''
    register_blue_Note(app)
    register_blue_Group(app)
    register_blue_Img(app)

def forward_note_error(error: TypeError):
    '''
    转发 Note 模块的错误
    '''
    return register_note_error_handler(error)