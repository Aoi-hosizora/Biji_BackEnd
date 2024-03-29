from flask import Blueprint

from app.controller import AuthCtrl, GroupCtrl, NoteCtrl, StarCtrl, ScheduleCtrl, DocumentCtrl, DocClassCtrl, RawCtrl, ShareDocCtrl
from app.middleware import AuthMw

from flask.app import Flask


# https://github.com/Aoi-hosizora/Biji_Baibuti/blob/master/app/src/main/java/com/baibuti/biji/model/dao/ServerApi.java

def setup_route_blue(app: Flask):
    """
    向 FlaskApp 注册每个模块的蓝图
    """
    auth = AuthMw.setup_auth()

    @app.route('/')
    def rootRoute():
        return {
            'message': 'Biji Api'
        }

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

    # Star Blue (1)
    blue_Star = Blueprint("blue_Star", __name__, url_prefix="/star")
    StarCtrl.apply_blue(blue_Star, auth)
    app.register_blueprint(blue_Star)

    # Schedule Blue (1)
    blue_Schedule = Blueprint("blue_Schedule", __name__, url_prefix="/schedule")
    ScheduleCtrl.apply_blue(blue_Schedule, auth)
    app.register_blueprint(blue_Schedule)

    # Document Blue (3)
    blue_DocClass = Blueprint("blue_DocClass", __name__, url_prefix="/docclass")
    DocClassCtrl.apply_blue(blue_DocClass, auth)
    app.register_blueprint(blue_DocClass)

    blue_Document = Blueprint("blue_Document", __name__, url_prefix="/document")
    DocumentCtrl.apply_blue(blue_Document, auth)
    app.register_blueprint(blue_Document)

    blue_DocShare = Blueprint("blue_DocShare", __name__, url_prefix="/share")
    ShareDocCtrl.apply_blue(blue_DocShare, auth)
    app.register_blueprint(blue_DocShare)

    # Raw
    blue_Raw = Blueprint("blue_Raw", __name__, url_prefix="/raw")
    RawCtrl.apply_blue(blue_Raw, auth)
    app.register_blueprint(blue_Raw)
