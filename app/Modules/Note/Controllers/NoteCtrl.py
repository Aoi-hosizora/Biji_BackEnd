from app.Database.NoteDAO import NoteDAO

from app.Modules.Note.Models.Note import Note
from app.Modules.Note.Exceptions.NoteNotExistError import NoteNotExistError
from app.Modules.Note.Exceptions.NoteUpdateError import NoteUpdateError
from app.Modules.Note.Exceptions.NoteInsertError import NoteInsertError
from app.Modules.Note.Exceptions.NoteDeleteError import NoteDeleteError

def getAllNotes(username: str) -> []:
    noteDao = NoteDAO()
    return noteDao.queryUserAllNotes(username)

def getOneNote(username: str, id: int) -> {}:
    noteDao = NoteDAO()
    ret = noteDao.queryUserOneNote(username, id)
    if ret == None:
        raise NoteNotExistError(id)
    return ret

def updateNote(username: str, note: Note) -> bool:
    noteDao = NoteDAO()
    if noteDao.updateUserNote(username, note):
        return True
    else:
        raise NoteUpdateError(note.id)

def insertNote(username: str, note: Note) -> bool:
    noteDao = NoteDAO()
    if noteDao.insertUserNote(username, note):
        return True
    else:
        raise NoteInsertError(note.title)

def deleteNote(username: str, note: Note) -> bool:
    noteDao = NoteDAO()
    if noteDao.deleteUserNote(username, note):
        return True
    else:
        raise NoteDeleteError(note.title)
