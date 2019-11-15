import json

from flask import Blueprint, request, g
from flask_httpauth import HTTPTokenAuth

from app.database.DbErrorType import DbErrorType
from app.database.dao.NoteDao import NoteDao
from app.model.po.Note import Note
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/note`
    """

    @auth.login_required
    @blue.route("/", methods=['GET'])
    def GetAllRoute():
        """
        所有笔记
        """
        notes = NoteDao().queryAllNotes(uid=g.user)
        return Result.ok().setData(Note.to_jsons(notes)).json_ret()

    @auth.login_required
    @blue.route("/group/<int:gid>", methods=['GET'])
    def GetByGidRoute(gid: int):
        """
        gid 查询笔记
        """
        notes = NoteDao().queryAllNotesByGroupId(uid=g.user, gid=gid)
        return Result.ok().setData(Note.to_jsons(notes)).json_ret()

    @auth.login_required
    @blue.route("/<int:nid>", methods=['GET'])
    def GetByIdRoute(nid: int):
        """
        nid 查询笔记
        """
        note = NoteDao().queryNoteById(uid=g.user, nid=nid)
        if not note:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Note Not Found").json_ret()
        return Result.ok().setData(note.to_json()).json_ret()

    @auth.login_required
    @blue.route("/", methods=['POST'])
    def InsertRoute():
        """
        插入
        """
        rawJson = json.loads(request.get_data(as_text=True))
        note = Note.from_json(rawJson)
        ret = NoteDao().insertNote(uid=g.user, note=note)
        if ret == DbErrorType.FOUNDED:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Note Existed").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Note Insert Failed").json_ret()
        else:  # Success
            return Result.ok().setData(note.to_json()).json_ret()

    @auth.login_required
    @blue.route("/", methods=['PUT'])
    def UpdateRoute():
        """
        更新
        """
        rawJson = json.loads(request.get_data(as_text=True))
        note = Note.from_json(rawJson)
        ret = NoteDao().updateNote(uid=g.user, note=note)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Group Update Failed").json_ret()
        else:  # Success
            return Result.ok().setData(note.to_json()).json_ret()

    @auth.login_required
    @blue.route("/<int:nid>", methods=['DELETE'])
    def DeleteRoute(nid: int):
        """
        删除
        """
        ret = NoteDao().deleteNote(uid=g.user, nid=nid)
        if ret == DbErrorType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Group Not Found").json_ret()
        elif ret == DbErrorType.FAILED:
            return Result.error().setMessage("Group Delete Failed").json_ret()
        else:  # Success
            return Result.ok().json_ret()
