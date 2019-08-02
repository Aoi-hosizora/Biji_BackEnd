from app.Utils import ErrorUtil, RespUtil
from app.Models.Message import Message

from app.Modules.Note.Controllers import NoteCtrl, GroupCtrl

from flask import Blueprint, request
from flask.app import Flask
import json

blue_Group = Blueprint("blue_Group", __name__, url_prefix="/group")
def register_blue_Group(app: Flask):
    app.register_blueprint(blue_Group)

@blue_Group.route("/", methods=["GET"])
def r():
    username = RespUtil.getAuthUser(request.headers)
    test = GroupCtrl.test(username=username)
    return RespUtil.jsonRet(
        dict=test, 
        code=ErrorUtil.Success
    )