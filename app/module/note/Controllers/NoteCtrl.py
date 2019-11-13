from app.database.NoteDAO import NoteDao
from app.module.log.Controllers import LogCtrl

from app.module.note.Models.Note import Note
from app.module.note.Exceptions.NotExistError import NotExistError
from app.module.note.Exceptions.UpdateError import UpdateError
from app.module.note.Exceptions.InsertError import InsertError
from app.module.note.Exceptions.DeleteError import DeleteError
from app.util.exception.BodyRawJsonError import BodyRawJsonError

import json

def getNoteFromReqData(reqdata: str) -> Note:
    '''
    从 Req 的 headers 中获取 Note

    `getNoteFromReqData(request.get_data(as_text=True))`
    '''
    try:
        postjson = json.loads(reqdata)
    except:
        # 解析错误
        raise BodyRawJsonError()
    
    return checkJson(postjson)
    
def getNotesFromReqData(reqdata: str) -> [Note]:
    '''
    从 Req 的 headers 中获取 Note[]

    `getNotesFromReqData(request.get_data(as_text=True))`
    '''
    try:
        postjsons = json.loads(reqdata)
        
        ret = []
        for postjson in postjsons:
            ret.append(checkJson(json.loads(postjson)))
    
    except:
        # 解析错误
        raise BodyRawJsonError()
    
    return ret

def checkJson(postjson) -> Note:
    '''
    检查 Json 并转化
    '''
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
    noteDao = NoteDao()
    return noteDao.queryAllNotes(username)

def getOneNote(username: str, id: int) -> Note:
    '''
    查询一个笔记
    '''
    noteDao = NoteDao()
    ret = noteDao.queryNoteById(username, id)
    if ret == None:
        raise NotExistError(id)
    return ret

def updateNote(username: str, note: Note) -> bool:
    '''
    更新一个旧笔记
    '''
    noteDao = NoteDao()
    if noteDao.updateNote(username, note):
        LogCtrl.updateNoteLog(username)
        return True
    else:
        raise UpdateError(note.id)

def insertNote(username: str, note: Note) -> bool:
    '''
    插入一个新笔记
    '''
    noteDao = NoteDao()
    if noteDao.insertNote(username, note):
        LogCtrl.updateNoteLog(username)
        return True
    else:
        raise InsertError(note.title)

def deleteNote(username: str, note: Note) -> bool:
    '''
    删除一个旧笔记
    '''
    noteDao = NoteDao()
    if noteDao.deleteNote(username, note):
        LogCtrl.updateNoteLog(username)
        return True
    else:
        raise DeleteError(note.title)

def pushNote(username: str, notes: [Note]) -> bool:
    '''
    同步笔记
    '''
    noteDao = NoteDao()
    rets = noteDao.queryAllNotes(username)
    r = False
    for ret in rets:
        r = noteDao.deleteNote(username, ret)
    
    for note in notes:
        r = noteDao.insertNote(username, note)
    
    return r
