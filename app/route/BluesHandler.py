from app import controller

from flask.app import Flask


def register_modules_blue(app: Flask):
    """
    向 FlaskApp 注册每个模块的蓝图
    """
    controller.register_auth_module_blue(app)
    controller.register_note_module_blue(app)
    controller.register_star_module_blue(app)
    controller.register_schedule_module_blue(app)
    controller.register_file_module_blue(app)
