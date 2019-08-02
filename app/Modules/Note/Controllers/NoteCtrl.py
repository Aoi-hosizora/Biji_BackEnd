from app.Database.NoteDAO import NoteDAO

from app.Modules.Note.Models.Note import Note

def getAllNotes(username: str) -> []:
    noteDao = NoteDAO()
    rets = noteDao.queryUserAllNotes(username)
    sets = []
    for ret in rets:
        note = Note(ret[1], ret[2], ret[3], ret[4], ret[5], ret[6])
        sets.append(note)
    return sets

def getOneNote(username: str, id: int) -> {}:
    noteDao = NoteDAO()
    rets = noteDao.queryUserOneNote(username, id)
    return Note(ret[1], ret[2], ret[3], ret[4], ret[5], ret[6])