from app.Utils import ErrorUtil, RespUtil, PassUtil
from app.Models.Message import Message
from app.Utils.Exceptions.PostFormKeyError import PostFormKeyError
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
    try:
        id = int(id)
    except:
        raise QueryError(list(['id']))
        
    notes = NoteCtrl.getOneNote(username=username, id=id)
    return RespUtil.jsonRet(
        dict=notes.toJson(), 
        code=ErrorUtil.Success
    )

@blue_Note.route("/update", methods=['Post'])
def UpdateNoteRoute():
    username = RespUtil.getAuthUser(request.headers)
    try:
        postjson = json.loads(request.get_data(as_text=True))

        keys = ['id', 'title', 'content', 'group_id', 'create_time', 'update_time']
        nonePostKeys = [
            key for key in keys
            if key not in postjson or postjson[key] == None
        ]
        if not len(nonePostKeys) == 0:
            raise(PostFormKeyError(nonePostKeys))

        note = Note(*[postjson[key] for key in keys])
    except:
        raise PostFormKeyError()

    NoteCtrl.updateNote(username=username, note=note)
    return RespUtil.jsonRet(
        dict=note.toJson(), 
        code=ErrorUtil.Success
    )

@blue_Note.route("/insert", methods=['Put'])
def InsertNoteRoute():
    username = RespUtil.getAuthUser(request.headers)
    try:
        postjson = json.loads(request.get_data(as_text=True))

        keys = ['id', 'title', 'content', 'group_id', 'create_time', 'update_time']
        nonePostKeys = [
            key for key in keys
            if key not in postjson or postjson[key] == None
        ]
        if not len(nonePostKeys) == 0:
            raise(PostFormKeyError(nonePostKeys))

        note = Note(*[postjson[key] for key in keys])
    except:
        raise PostFormKeyError()

    NoteCtrl.insertNote(username=username, note=note)
    return RespUtil.jsonRet(
        dict=note.toJson(), 
        code=ErrorUtil.Success
    )

@blue_Note.route("/delete", methods=['Delete'])
def DeleteNoteRoute():
    username = RespUtil.getAuthUser(request.headers)
    try:
        postjson = json.loads(request.get_data(as_text=True))

        keys = ['id', 'title', 'content', 'group_id', 'create_time', 'update_time']
        nonePostKeys = [
            key for key in keys
            if key not in postjson or postjson[key] == None
        ]
        if not len(nonePostKeys) == 0:
            raise(PostFormKeyError(nonePostKeys))

        note = Note(*[postjson[key] for key in keys])
    except:
        raise PostFormKeyError()

    NoteCtrl.deleteNote(username=username, note=note)
    return RespUtil.jsonRet(
        dict=note.toJson(), 
        code=ErrorUtil.Success
    )