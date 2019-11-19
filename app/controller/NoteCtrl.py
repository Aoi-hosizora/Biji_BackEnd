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

    @blue.route("/", methods=['GET'])
    @auth.login_required
    def GetAllRoute():
        """ 所有笔记 """
        notes = NoteDao().queryAllNotes(uid=g.user)
        return Result.ok().setData(Note.to_jsons(notes)).json_ret()

    @blue.route("/group/<int:gid>", methods=['GET'])
    @auth.login_required
    def GetByGidRoute(gid: int):
        """ gid 查询笔记 """
        notes = NoteDao().queryAllNotesByGroupId(uid=g.user, gid=gid)
        return Result.ok().setData(Note.to_jsons(notes)).json_ret()

    @blue.route("/<int:nid>", methods=['GET'])
    @auth.login_required
    def GetByIdRoute(nid: int):
        """ nid 查询笔记 """
        note = NoteDao().queryNoteById(uid=g.user, nid=nid)
        if not note:
            return Result.error(ResultCode.NOT_FOUND).setMessage("Note Not Found").json_ret()
        return Result.ok().setData(note.to_json()).json_ret()

    #######################################################################################################################

    @blue.route("/", methods=['POST'])
    @auth.login_required
    def InsertRoute():
        """ 插入 """
        try:
            req_title = request.form['title']
            req_content = request.form['content']
            req_group_id = int(request.form['group_id'])
            req_ct = request.form['create_time']
            req_ut = request.form['update_time']
        except:
            raise ParamError(ParamType.FORM)
        if not (Config.FMT_NOTE_TITLE_MIN <= len(req_title) <= Config.FMT_NOTE_TITLE_MAX):
            return Result().error(ResultCode.BAD_REQUEST).setMessage('Format Error').json_ret()
        req_note = Note(nid=-1, title=req_title, content=req_content, group=req_group_id, create_time=req_ct, update_time=req_ut)

        status, new_note = NoteDao().insertNote(uid=g.user, note=req_note)
        if status == DbStatusType.FOUNDED:
            return Result.error(ResultCode.HAS_EXISTED).setMessage("Note Existed").json_ret()
        elif status == DbStatusType.FAILED or not new_note:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Note Insert Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_note.to_json()).json_ret()

    @blue.route("/", methods=['PUT'])
    @auth.login_required
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
        elif status == DbStatusType.FAILED or not new_note:
            return Result.error(ResultCode.DATABASE_FAILED).setMessage("Note Update Failed").json_ret()
        else:  # Success
            return Result.ok().setData(new_note.to_json()).json_ret()

    @blue.route("/<int:nid>", methods=['DELETE'])
    @auth.login_required
    def DeleteRoute(nid: int):
        """ 删除 """
        note: Note = NoteDao().queryNoteById(uid=g.user, nid=nid)
        count = NoteDao().deleteNotes(uid=g.user, ids=[nid])
        if count == 0 or not note:
            return Result().error(ResultCode.NOT_FOUND).setMessage("Note Not Found").json_ret()
        elif count == -1:
            return Result().error(ResultCode.DATABASE_FAILED).setMessage("Note Delete Failed").json_ret()
        else:
            return Result().ok().setData(note.to_json()).json_ret()

    @blue.route("/", methods=['DELETE'])
    @auth.login_required
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
