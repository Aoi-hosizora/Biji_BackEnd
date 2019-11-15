from app.database.dao.DocumentClassDao import DocumentClassDao
from app.route.exception.BodyRawJsonError import BodyRawJsonError
from app.module.log.Controllers import LogCtrl

from app.model.po.DocumentClass import DocumentClass
from app.controller.file.exception.UpdateError import UpdateError
from app.controller.file.exception.InsertError import InsertError
from app.controller.file.exception.DeleteError import DeleteError

import json

def getFileClassFromReqData(reqdata: str) -> DocumentClass:

    try:
        postjson = json.loads(reqdata)
    except:
        raise BodyRawJsonError()

    return checkJson(postjson)

def getFileClassesFromReqData(reqdata: str) -> [DocumentClass]:

    try:
        postjsons = json.loads(reqdata)

        ret = []
        for postjson in postjsons:
            ret.append(checkJson(json.loads(postjson)))

    except:
        raise BodyRawJsonError()

    return ret

def checkJson(postjson) -> DocumentClass:
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
        return DocumentClass(*[postjson[key] for key in keys])
    except:
        raise BodyRawJsonError()

def getAllFileClasses(username: str) -> [DocumentClass]:
    '''
    查询所有文件分类
    '''
    fileClassDao = DocumentClassDao()
    return fileClassDao.queryAllDocumentClasses(username)

def getOneFileClass(username: str, fileClass: DocumentClass) -> DocumentClass:
    '''
    查询一个文件分类
    '''
    fileClassDao = DocumentClassDao()
    ret = fileClassDao.queryDefaultDocumentClass(username, fileClass)
    return ret

def updateFileClass(username: str, fileClass: DocumentClass) -> bool:
    '''
    更新一个旧分类
    '''
    fileClassDao = DocumentClassDao()
    if fileClassDao.updateDocumentClass(username, fileClass):
        LogCtrl.updateFileClassLog(username)
        return True
    else:
        raise UpdateError(fileClass.name)
        
def insertFileClass(username: str, fileClass: DocumentClass) -> bool:
    '''
    插入一个新分类
    '''
    fileClassDao = DocumentClassDao()
    if fileClassDao.insertDocumentClass(username, fileClass):
        LogCtrl.updateFileClassLog(username)
        return True
    else:
        raise InsertError(fileClass.name, False)

def deleteFileClass(username: str, fileClass: DocumentClass) -> bool:
    '''
    删除一个旧分类
    '''
    fileClassDao = DocumentClassDao()
    if fileClassDao.deleteDocumentClass(username, fileClass):
        LogCtrl.updateFileClassLog(username)
        return True
    else:
        raise DeleteError(fileClass.name, False)
    
def pushFileClass(username: str, fileClasses: [DocumentClass]) -> bool:
    '''
    同步分类
    '''
    fileClassDao = DocumentClassDao()
    r = True

    for fileClass in fileClasses:
        if fileClassDao.queryDefaultDocumentClass(username, fileClass) is None:
            r = insertFileClass(username, fileClass)
    
    return r

def shareCode2Json(username: str, foldername: str):
    return "{\"usr\":\""+username+"\",\"folder\":\""+foldername+"\"}"
