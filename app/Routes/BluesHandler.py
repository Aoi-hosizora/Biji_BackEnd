from app.Modules import Auth
from app.Modules import Note
from app.Modules import Star
from app.Modules import File
from app.Modules import Schedule
from app.Modules import Log

from flask.app import Flask

def register_modules_blue(app: Flask):
    '''
    向 FlaskApp 注册每个模块的蓝图
    '''    
    Auth.register_auth_blue(app)
    Note.register_note_blue(app)
    Star.register_star_blue(app)
    File.register_file_blue(app)
    Schedule.register_schedule_blue(app)
    Log.register_log_blue(app)
