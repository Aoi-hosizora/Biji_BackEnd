from app.Database.FileClassDAO import FileClassDAO
from app.Utils.Exceptions.BodyRawJsonError import BodyRawJsonError
from app.Modules.Log.Controllers import LogCtrl

from app.Modules.File.Models.FileClass import FileClass
from app.Modules.File.Exceptions.FileClassNotExistError import FileClassNotExistError
from app.Modules.File.Exceptions.UpdateError import UpdateError
from app.Modules.File.Exceptions.InsertError import InsertError
from app.Modules.File.Exceptions.DeleteError import DeleteError

import json

def getFileClassFromReqData(reqdata: str) -> FileClass:

    try:
        postjson = json.loads(reqdata)
    except:
        raise BodyRawJsonError()

    return checkJson(postjson)

def getFileClassesFromReqData(reqdata: str) -> [FileClass]:

    try:
        postjsons = json.loads(reqdata)

        ret = []
        for postjson in postjsons:
            ret.append(checkJson(json.loads(postjson)))

    except:
        raise BodyRawJsonError()

    return ret

def checkJson(postjson) -> FileClass:
    '''
    检查 Json 并转换
    '''
    keys = ['id', 'name']
    nonePostKeys = [
        key for key in keys
        if key not in postjson or postjson[key] == None
    ]
    if not len(nonePostKeys) == 0:
        raise(BodyRawJsonError(nonePostKeys))
    try:
        return FileClass(*[postjson[key] for key in keys])
    except:
        raise BodyRawJsonError()

def getAllFileClasses(username: str) -> [FileClass]:
    '''
    查询所有文件分类
    '''
    fileClassDao = FileClassDAO()
    return fileClassDao.queryUserAllFileClasses(username)

def getOneFileClass(username: str, id: int) -> FileClass:
    '''
    查询一个文件分类
    '''
    fileClassDao = FileClassDAO()
    ret = fileClassDao.queryUserOneFileClass(username, id)
    if ret == None:
        raise FileClassNotExistError(username)
    return ret

def updateFileClass(username: str, fileClass: FileClass) -> bool:
    '''
    更新一个旧分类
    '''
    fileClassDao = FileClassDAO()
    if fileClassDao.updateUserFileClass(username, fileClass):
        LogCtrl.updateFileClassLog(username)
        return True
    else:
        raise UpdateError(fileClass.name)
        
def insertFileClass(username: str, fileClass: FileClass) -> bool:
    '''
    插入一个新分类
    '''
    fileClassDao = FileClassDAO()
    if fileClassDao.insertUserFileClass(username, fileClass):
        LogCtrl.updateFileClassLog(username)
        return True
    else:
        raise InsertError(fileClass.name, False)

def deleteFileClass(username: str, fileClass: FileClass) -> bool:
    '''
    删除一个旧分类
    '''
    fileClassDao = FileClassDAO()
    if fileClassDao.deleteUserFileClass(username, fileClass):
        LogCtrl.updateFileClassLog(username)
        return True
    else:
        raise DeleteError(fileClass.name, False)
    
def pushFileClass(username: str, fileClasses: [FileClass]) -> bool:
    '''
    同步分类
    '''
    fileClassDao = FileClassDAO()
    rets = fileClassDao.queryUserAllFileClasses(username)
    r = True
    for ret in rets:
        r = fileClassDao.deleteUserFileClass(username, ret)
    
    for fileClass in fileClasses:
        r = fileClassDao.insertUserFileClass(username, fileClass)
    
    return r