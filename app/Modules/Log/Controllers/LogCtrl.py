from app.Modules.Log.Models.Log import Log
from app.Database.LogDAO import LogDAO

import json
from app.Utils.Exceptions.BodyRawJsonError import BodyRawJsonError

def getLogFromReqData(reqdata: str) -> Log:
    '''
    从 Req 的 headers 中获取 Log

    `getLogFromReqData(request.headers)`
    '''
    try:
        postjson = json.loads(reqdata)
    except:
        # 解析错误
        raise BodyRawJsonError()

    keys = ['module', 'ut']
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
        return Log(*[postjson[key] for key in keys])
    except:
        # 内容错误
        raise BodyRawJsonError()

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


def updateLog(username: str, log: Log) -> bool:
    '''
    同步来自客户端的日志
    '''
    logDao = LogDAO()
    return logDao.updateUserLog(username, log.module, log.updateTime)

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