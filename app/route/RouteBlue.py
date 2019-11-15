from flask import Blueprint

from app.controller import AuthCtrl, GroupCtrl, NoteCtrl, StarCtrl
from app.middleware import AuthMw

from flask.app import Flask


# https://github.com/Aoi-hosizora/Biji_Baibuti/blob/master/app/src/main/java/com/baibuti/biji/model/dao/ServerApi.java

def setup_route_blue(app: Flask):
    """
    向 FlaskApp 注册每个模块的蓝图
    """
    auth = AuthMw.setup_auth()

    # Auth Blue (1)
    blue_Auth = Blueprint("blue_Auth", __name__, url_prefix="/auth")
    AuthCtrl.apply_blue(blue_Auth, auth)
    app.register_blueprint(blue_Auth)

    # Note Blue (2)
    blue_Group = Blueprint("blue_Group", __name__, url_prefix="/group")
    GroupCtrl.apply_blue(blue_Group, auth)
    app.register_blueprint(blue_Group)

    blue_Note = Blueprint("blue_Note", __name__, url_prefix="/note")
    NoteCtrl.apply_blue(blue_Note, auth)
    app.register_blueprint(blue_Note)

    # Star Blue
    blue_Star = Blueprint("blue_Star", __name__, url_prefix="/star")
    StarCtrl.apply_blue(blue_Star, auth)
    app.register_blueprint(blue_Star)

    # controller.register_schedule_module_blue(app)
    # controller.register_file_module_blue(app)
