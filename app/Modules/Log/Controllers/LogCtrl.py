from app.Modules.Log.Models.Log import Log
from app.Database.LogDAO import LogDAO

def getUserAllLog(username: str) -> [Log]:
    '''
    获得用户所有日志
    '''
    logDao = LogDAO()
    return logDao.queryUserAllLogs(username)

def getNoteLog(username: str) -> Log:
    '''
    获得用户笔记的更新日志
    '''
    logDao = LogDAO()
    return logDao.queryUserOneLog(username, logDao.mod_note)

def getGroupLog(username: str) -> Log:
    '''
    获得用户分组的更新日志
    '''
    logDao = LogDAO()
    return logDao.queryUserOneLog(username, logDao.mod_group)

def getStarLog(username: str) -> Log:
    '''
    获得用户收藏的更新日志
    '''
    logDao = LogDAO()
    return logDao.queryUserOneLog(username, logDao.mod_star)

def getScheduleLog(username: str) -> Log:
    '''
    获得用户课程的更新日志
    '''
    logDao = LogDAO()
    return logDao.queryUserOneLog(username, logDao.mod_schedule)

def getFileLog(username: str) -> Log:
    '''
    获得用户文件的更新日志
    '''
    logDao = LogDAO()
    return logDao.queryUserOneLog(username, logDao.mod_file)



def updateNoteLog(username: str) -> bool:
    '''
    更新用户笔记的更新日志
    '''
    logDao = LogDAO()
    return logDao.updateUserLog(username, logDao.mod_note)

def updateGroupLog(username: str) -> bool:
    '''
    更新用户分组的更新日志
    '''
    logDao = LogDAO()
    return logDao.updateUserLog(username, logDao.mod_group)

def updateStarLog(username: str) -> bool:
    '''
    更新用户收藏的更新日志
    '''
    logDao = LogDAO()
    return logDao.updateUserLog(username, logDao.mod_star)

def updateScheduleLog(username: str) -> bool:
    '''
    更新用户课程的更新日志
    '''
    logDao = LogDAO()
    return logDao.updateUserLog(username, logDao.mod_schedule)

def updateFileLog(username: str) -> bool:
    '''
    更新用户文件的更新日志
    '''
    logDao = LogDAO()
    return logDao.updateUserLog(username, logDao.mod_file)