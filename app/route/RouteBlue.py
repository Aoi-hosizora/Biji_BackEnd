from flask import Blueprint

from app.controller import AuthCtrl, GroupCtrl, NoteCtrl
from app.middleware import AuthMw

from flask.app import Flask


# https://github.com/Aoi-hosizora/Biji_Baibuti/blob/master/app/src/main/java/com/baibuti/biji/model/dao/ServerApi.java

def register_modules_blue(app: Flask):
    """
    向 FlaskApp 注册每个模块的蓝图
    """
    auth = AuthMw.setup_auth()

    # Auth Blue (1)
    blue_Auth = Blueprint("blue_Auth", __name__, url_prefix="/auth")
    AuthCtrl.apply_blue(blue_Auth, auth)
    app.register_blueprint(blue_Auth)

    # Note Blue (3)
    blue_Group = Blueprint("blue_Group", __name__, url_prefix="/group")
    GroupCtrl.apply_blue(blue_Group, auth)
    app.register_blueprint(blue_Group)

    blue_Note = Blueprint("blue_Note", __name__, url_prefix="/note")
    NoteCtrl.apply_blue(blue_Note, auth)
    app.register_blueprint(blue_Note)

    # controller.register_auth_module_blue(app)
    # controller.register_note_module_blue(app)
    # controller.register_star_module_blue(app)
    # controller.register_schedule_module_blue(app)
    # controller.register_file_module_blue(app)
