from app.Database.NoteDAO import NoteDAO
from app.Modules.Log.Controllers import LogCtrl

from app.Modules.Note.Models.Note import Note
from app.Modules.Note.Exceptions.NotExistError import NotExistError
from app.Modules.Note.Exceptions.UpdateError import UpdateError
from app.Modules.Note.Exceptions.InsertError import InsertError
from app.Modules.Note.Exceptions.DeleteError import DeleteError
from app.Utils.Exceptions.BodyRawJsonError import BodyRawJsonError

import json

def getNoteFromReqData(reqdata: str) -> Note:
    '''
    从 Req 的 headers 中获取 Note

    `getNoteFromReqData(request.headers)`
    '''
    try:
        postjson = json.loads(reqdata)
    except:
        # 解析错误
        raise BodyRawJsonError()

    keys = ['id', 'title', 'content', 'group_id', 'create_time', 'update_time']
    nonePostKeys = [
        key for key in keys
        if key not in postjson or postjson[key] == None
    ]
    if not len(nonePostKeys) == 0:
        # 缺少参数
        raise(BodyRawJsonError(nonePostKeys))

    if not len(postjson) == len(keys):
        # 参数过多
        raise BodyRawJsonError()

    try:
        return Note(*[postjson[key] for key in keys])
    except:
        # 内容错误
        raise BodyRawJsonError()

def getAllNotes(username: str) -> [Note]:
    '''
    查询所有笔记
    '''
    noteDao = NoteDAO()
    return noteDao.queryUserAllNotes(username)

def getOneNote(username: str, id: int) -> Note:
    '''
    查询一个笔记
    '''
    noteDao = NoteDAO()
    ret = noteDao.queryUserOneNote(username, id)
    if ret == None:
        raise NotExistError(id)
    return ret

def updateNote(username: str, note: Note) -> bool:
    '''
    更新一个旧笔记
    '''
    noteDao = NoteDAO()
    if noteDao.updateUserNote(username, note):
        LogCtrl.updateNoteLog(username)
        return True
    else:
        raise UpdateError(note.id)

def insertNote(username: str, note: Note) -> bool:
    '''
    插入一个新笔记
    '''
    noteDao = NoteDAO()
    if noteDao.insertUserNote(username, note):
        LogCtrl.updateNoteLog(username)
        return True
    else:
        raise InsertError(note.title)

def deleteNote(username: str, note: Note) -> bool:
    '''
    删除一个旧笔记
    '''
    noteDao = NoteDAO()
    if noteDao.deleteUserNote(username, note):
        LogCtrl.updateNoteLog(username)
        return True
    else:
        raise DeleteError(note.title)
