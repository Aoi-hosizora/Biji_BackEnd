from app.Utils import ErrorUtil, RespUtil, PassUtil
from app.Models.Message import Message
from app.Utils.Exceptions.QueryError import QueryError

from app.Modules.Note.Controllers import NoteCtrl
from app.Modules.Note.Models.Note import Note

from flask import Blueprint, request
from flask.app import Flask
import json

blue_Note = Blueprint("blue_Note", __name__, url_prefix="/note")
def register_blue_Note(app: Flask):
    app.register_blueprint(blue_Note)

@blue_Note.route("/all", methods=['GET'])
def AllNoteRoute():
    username = RespUtil.getAuthUser(request.headers)
    notes = NoteCtrl.getAllNotes(username=username)
    return RespUtil.jsonRet(
        dict=Note.toJsonSet(notes), 
        code=ErrorUtil.Success
    )

@blue_Note.route("/one", methods=['GET'])
def OneNoteRoute():
    username = RespUtil.getAuthUser(request.headers)
    id = request.args.get('id')
    if id == None:
        raise QueryError(['id'])
        
    notes = NoteCtrl.getOneNote(username=username)
    return RespUtil.jsonRet(
        dict=Note.toJsonSet(notes), 
        code=ErrorUtil.Success
    )