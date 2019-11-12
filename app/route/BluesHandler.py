from app.module import auth
from app.module import note
from app.module import star
from app.module import file
from app.module import schedule
from app.module import log

from flask.app import Flask


def register_modules_blue(app: Flask):
    """
    向 FlaskApp 注册每个模块的蓝图
    """
    auth.register_auth_blue(app)
    note.register_note_blue(app)
    star.register_star_blue(app)
    file.register_file_blue(app)
    schedule.register_schedule_blue(app)
    log.register_log_blue(app)
