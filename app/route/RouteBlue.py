from flask import Blueprint

from app.controller import AuthCtrl

from flask.app import Flask

from app.middleware import AuthMw


def register_modules_blue(app: Flask):
    """
    向 FlaskApp 注册每个模块的蓝图
    """
    auth = AuthMw.setup_auth()

    blue_Auth = Blueprint("blue_Auth", __name__, url_prefix="/auth")
    AuthCtrl.apply_blue(blue_Auth, auth)
    app.register_blueprint(blue_Auth)

    # controller.register_auth_module_blue(app)
    # controller.register_note_module_blue(app)
    # controller.register_star_module_blue(app)
    # controller.register_schedule_module_blue(app)
    # controller.register_file_module_blue(app)
