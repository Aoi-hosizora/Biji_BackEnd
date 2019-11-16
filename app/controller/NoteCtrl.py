from typing import List

from flask import Blueprint, request, g
from flask_httpauth import HTTPTokenAuth

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.dao.NoteDao import NoteDao
from app.model.po.Note import Note
from app.model.dto.Result import Result
from app.model.dto.ResultCode import ResultCode
from app.route.ParamType import ParamError, ParamType


def apply_blue(blue: Blueprint, auth: HTTPTokenAuth):
    """
    应用 Blueprint Endpoint 路由映射 `/note`
    """

    @auth.login_required
    @blue.route("/", methods=['GET'])
    def GetAllRoute():
        """ 所有笔记 """
        notes = NoteDao().queryAllNotes(uid=g.user)
        return Result.ok().setData(Note.to_jsons(notes)).json_ret()

    @auth.login_required
    @blue.route("/group/<int:gid>", methods=['GET'])
    def GetByGidRoute(gid: int):
        """ gid 查询笔记 """
        notes = NoteDao().queryAllNotesByGroupId(uid=g.user, gid=gid)
        return Result.ok().setData(Note.to_jsons(notes)).json_ret()

    @auth.login_required
    @blue.route("/<int:nid>", methods=['GET'])
    def GetByIdRoute(nid: int):
        """ nid 查询笔记 """
        note = NoteDao().queryNoteById(uid=g.user, nid=nid)
        if not note:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Note Not Found").json_ret()
        return Result.ok().setData(note.to_json()).json_ret()

    #######################################################################################################################

    @auth.login_required
    @blue.route("/", methods=['POST'])
    def InsertRoute():
        """ 插入 """
        try:
            req_title = request.form['title']
            req_content = request.form['content']
            req_group_id = int(request.form['group_id'])
        except:
            raise ParamError(ParamType.FORM)
        if not (Config.FMT_NOTE_TITLE_MIN <= len(req_title) <= Config.FMT_NOTE_TITLE_MAX):
            return Result().error(ResultCode.BAD_REQUEST).setMessage('Format Error').json_ret()
        req_note = Note(nid=-1, title=req_title, content=req_content, group=req_group_id)

        status, new_note = NoteDao().insertNote(uid=g.user, note=req_note)
        if status == DbStatusType.FOUNDED:
            return Result.error(ResultCode.HAS_EXISTED).setMessage("Note Existed").json_ret()
        elif status == DbStatusType.FAILED or not new_note:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Note Insert Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_note.to_json()).json_ret()

    @auth.login_required
    @blue.route("/", methods=['PUT'])
    def UpdateRoute():
        """ 更新 """
        try:
            req_id = int(request.form['id'])
            req_title = request.form['title']
            req_content = request.form['content']
            req_group_id = int(request.form['group_id'])
        except:
            raise ParamError(ParamType.FORM)
        if not (Config.FMT_NOTE_TITLE_MIN <= len(req_title) <= Config.FMT_NOTE_TITLE_MAX):
            return Result().error(ResultCode.BAD_REQUEST).setMessage('Format Error').json_ret()
        req_note = Note(nid=req_id, title=req_title, content=req_content, group=req_group_id)

        status, new_note = NoteDao().updateNote(uid=g.user, note=req_note)
        if status == DbStatusType.NOT_FOUND:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Note Not Found").json_ret()
        elif status == DbStatusType.FAILED:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Note Update Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_note.to_json()).json_ret()

    @auth.login_required
    @blue.route("/<int:uid>", methods=['DELETE'])
    def DeleteRoute(uid: int):
        """ 删除 """
        count = NoteDao().deleteNotes(uid=g.user, ids=[uid])
        if count == 0:
            return Result().error(ResultCode.NOT_FOUND).setMessage("Note Not Found").json_ret()
        elif count == -1:
            return Result().error(ResultCode.DATABASE_FAILED).setMessage("Note Delete Failed").json_ret()
        else:
            return Result().ok().putData("count", count).json_ret()

    @auth.login_required
    @blue.route("/", methods=['DELETE'])
    def DeletesRoute():
        """ 删除多个 """
        req_ids: List = request.form.getlist('id')
        delete_ids: List[int] = []
        for req_id in req_ids:
            try:
                delete_ids.append(int(req_id))
            except KeyError:
                pass

        count = NoteDao().deleteNotes(uid=g.user, ids=delete_ids)
        if count == -1:
            return Result().error(ResultCode.DATABASE_FAILED).setMessage("Note Delete Failed").json_ret()
        else:
            return Result().ok().putData("count", count).json_ret()
