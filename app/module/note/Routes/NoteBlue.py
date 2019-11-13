from app.util import ErrorUtil, RespUtil
from app.model.dto.Message import Message
from app.util.exception.QueryError import QueryError

from app.module.note.Controllers import NoteCtrl
from app.model.po.Note import Note

from flask import Blueprint, request
from flask.app import Flask

blue_Note = Blueprint("blue_Note", __name__, url_prefix="/note")


def register_blue_Note(app: Flask):
    """
    注册笔记蓝图 `/note`

    `GET /all` `GET /one?id=<int>`
    `POST /update` `PUT /insert` `DELETE /delete`
    """
    app.register_blueprint(blue_Note)


@blue_Note.route("/all", methods=['GET'])
def AllNoteRoute():
    """
    获得所有笔记路由处理 `GET /all`
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    notes = NoteCtrl.getAllNotes(username=username)
    return RespUtil.jsonRet(
        data=Note.toJsonSet(notes),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Note.route("/one", methods=['GET'])
def OneNoteRoute():
    """
    获得单个笔记路由处理 `GET /one?id=<int>`
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    id = request.args.get('id')
    try:
        id = int(id)
    except Exception as ex:
        raise QueryError(list(['id']))

    note = NoteCtrl.getOneNote(username=username, id=id)
    return RespUtil.jsonRet(
        data=note.to_json(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Note.route("/update", methods=['POST'])
def UpdateNoteRoute():
    """
    更新笔记路由处理 `POST /update`

    @body `Note` JSON
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    note = NoteCtrl.getNoteFromReqData(request.get_data(as_text=True))

    NoteCtrl.updateNote(username=username, note=note)
    return RespUtil.jsonRet(
        data=note.to_json(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Note.route("/insert", methods=['PUT'])
def InsertNoteRoute():
    """
    插入笔记路由处理 `POST /insert`

    @body `Note` JSON
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    note = NoteCtrl.getNoteFromReqData(request.get_data(as_text=True))

    NoteCtrl.insertNote(username=username, note=note)
    return RespUtil.jsonRet(
        data=note.to_json(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Note.route("/delete", methods=['DELETE'])
def DeleteNoteRoute():
    """
    删除笔记路由处理 `POST /delete`

    @body `Note` JSON
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    note = NoteCtrl.getNoteFromReqData(request.get_data(as_text=True))

    NoteCtrl.deleteNote(username=username, note=note)
    return RespUtil.jsonRet(
        data=note.to_json(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )


@blue_Note.route("/push", methods=['POST'])
def PushNoteRoute():
    """
    同步笔记路由处理 `POST /push`

    @body `Note []` JSON
    """
    username, newToken = RespUtil.getAuthUser(request.headers)
    notes = NoteCtrl.getNotesFromReqData(request.get_data(as_text=True))

    NoteCtrl.pushNote(username, notes)
    return RespUtil.jsonRet(
        data=Message(message="Notes push finished", detail=len(notes)).toJson(),
        code=ErrorUtil.Success,
        headers={'Authorization': newToken} if newToken != "" else {}
    )
