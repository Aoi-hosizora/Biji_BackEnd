from app.Utils import ErrorUtil, RespUtil
from app.Models.Message import Message
from app.Utils.Exceptions.QueryError import QueryError

from app.Modules.Note.Controllers import NoteCtrl
from app.Modules.Note.Models.Note import Note

from flask import Blueprint, request
from flask.app import Flask
import json

blue_Note = Blueprint("blue_Note", __name__, url_prefix="/note")
def register_blue_Note(app: Flask):
    '''
    注册笔记蓝图 `/note`

    `GET /all` `GET /one?id=<int>`
    `POST /update` `PUT /insert` `DELETE /delete`
    '''
    app.register_blueprint(blue_Note)

@blue_Note.route("/all", methods=['GET'])
def AllNoteRoute():
    '''
    获得所有笔记路由处理 `GET /all`
    '''
    username = RespUtil.getAuthUser(request.headers)
    notes = NoteCtrl.getAllNotes(username=username)
    return RespUtil.jsonRet(
        dict=Note.toJsonSet(notes), 
        code=ErrorUtil.Success
    )

@blue_Note.route("/one", methods=['GET'])
def OneNoteRoute():
    '''
    获得单个笔记路由处理 `GET /one?id=<int>`
    '''
    username = RespUtil.getAuthUser(request.headers)
    id = request.args.get('id')
    try:
        id = int(id)
    except:
        raise QueryError(list(['id']))
        
    note = NoteCtrl.getOneNote(username=username, id=id)
    return RespUtil.jsonRet(
        dict=note.toJson(), 
        code=ErrorUtil.Success
    )

@blue_Note.route("/update", methods=['POST'])
def UpdateNoteRoute():
    '''
    更新笔记路由处理 `POST /update`
    
    @body `Note` JSON
    '''
    username = RespUtil.getAuthUser(request.headers)
    note = NoteCtrl.getNoteFromReqData(request.get_data(as_text=True))
    
    NoteCtrl.updateNote(username=username, note=note)
    return RespUtil.jsonRet(
        dict=note.toJson(), 
        code=ErrorUtil.Success
    )

@blue_Note.route("/insert", methods=['PUT'])
def InsertNoteRoute():
    '''
    插入笔记路由处理 `POST /insert`

    @body `Note` JSON
    '''
    username = RespUtil.getAuthUser(request.headers)
    note = NoteCtrl.getNoteFromReqData(request.get_data(as_text=True))
    
    NoteCtrl.insertNote(username=username, note=note)
    return RespUtil.jsonRet(
        dict=note.toJson(), 
        code=ErrorUtil.Success
    )

@blue_Note.route("/delete", methods=['DELETE'])
def DeleteNoteRoute():
    '''
    删除笔记路由处理 `POST /delete`

    @body `Note` JSON
    '''
    username = RespUtil.getAuthUser(request.headers)
    note = NoteCtrl.getNoteFromReqData(request.get_data(as_text=True))

    NoteCtrl.deleteNote(username=username, note=note)
    return RespUtil.jsonRet(
        dict=note.toJson(), 
        code=ErrorUtil.Success
    )