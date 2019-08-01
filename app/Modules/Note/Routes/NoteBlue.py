from app.Utils import ErrorUtil, RespUtil
from app.Models.Message import Message

from app.Modules.Note.Exceptions.NoteError import NoteError

from app.Modules.Note.Controllers import NoteCtrl

from flask import Blueprint, request
from flask.app import Flask
import json

blue_Note = Blueprint("blue_Note", __name__, url_prefix="/note")
def register_blue_Note(app: Flask):
    app.register_blueprint(blue_Note)

@blue_Note.route("/", methods=['GET'])
def test():
    return RespUtil.jsonRet(
        dict=NoteCtrl.getTestInfo().toJson(),
        code=ErrorUtil.Success
    )

@blue_Note.route("/err", methods=['GET'])
def err():
    raise NoteError("err")
