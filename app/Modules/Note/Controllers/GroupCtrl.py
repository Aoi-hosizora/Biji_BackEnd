from app.Database.GroupDAO import GroupDAO
from app.Utils.Exceptions.BodyRawJsonError import BodyRawJsonError
from app.Modules.Log.Controllers import LogCtrl

from app.Modules.Note.Models.Group import Group
from app.Modules.Note.Exceptions.NotExistError import NotExistError
from app.Modules.Note.Exceptions.UpdateError import UpdateError
from app.Modules.Note.Exceptions.InsertError import InsertError
from app.Modules.Note.Exceptions.DeleteError import DeleteError

import json

def getGroupFromReqData(reqdata: str) -> Group:
    '''
    从 Req 的 headers 中获取 Group

    `getGroupFromReqData(request.headers)`
    '''
    try:
        postjson = json.loads(reqdata)
    except:
        raise BodyRawJsonError()

    return checkJson(postjson)

def getGroupsFromReqData(reqdata: str) -> [Group]:
    '''
    从 Req 的 headers 中获取 Group[]

    `getGroupsFromReqData(request.headers)`
    '''
    try:
        postjsons = json.loads(reqdata)

        ret = []
        for postjson in postjsons:
            ret.append(checkJson(json.loads(postjson)))

    except:
        raise BodyRawJsonError()

    return ret

def checkJson(postjson) -> Group:
    '''
    检查 Json 并转换
    '''
    keys = ['id', 'name', 'order', 'color']
    nonePostKeys = [
        key for key in keys
        if key not in postjson or postjson[key] == None
    ]
    if not len(nonePostKeys) == 0:
        raise(BodyRawJsonError(nonePostKeys))
    try:
        return Group(*[postjson[key] for key in keys])
    except:
        raise BodyRawJsonError()

def getAllGroups(username: str) -> [Group]:
    '''
    查询所有分组
    '''
    groupDao = GroupDAO()
    return groupDao.queryUserAllGroups(username)

def getOneGroup(username: str, id: int) -> Group:
    '''
    查询一个分组
    '''
    groupDao = GroupDAO()
    ret = groupDao.queryUserOneGroup(username, id)
    if ret == None:
        raise NotExistError(id, isNote=False)
    return ret

def updateGroup(username: str, group: Group) -> bool:
    '''
    更新一个旧分组
    '''
    groupDao = GroupDAO()
    if groupDao.updateUserGroup(username, group):
        LogCtrl.updateNoteLog(username)
        return True
    else:
        raise UpdateError(group.id, isNote=False)
        
def insertGroup(username: str, group: Group) -> bool:
    '''
    插入一个新分组
    '''
    groupDao = GroupDAO()
    if groupDao.insertUserGroup(username, group):
        LogCtrl.updateNoteLog(username)
        return True
    else:
        raise InsertError(group.name, isNote=False)

def deleteGroup(username: str, group: Group) -> bool:
    '''
    删除一个旧分组
    '''
    groupDao = GroupDAO()
    if groupDao.deleteUserGroup(username, group):
        LogCtrl.updateNoteLog(username)
        return True
    else:
        raise DeleteError(group.name, isNote=False)
    
def pushGroup(username: str, groups: [Group]) -> bool:
    '''
    同步分组
    '''
    groupDao = GroupDAO()
    rets = groupDao.queryUserAllGroups(username)
    r = True
    for ret in rets:
        r = groupDao.deleteUserGroup(username, ret)
    
    for group in groups:
        r = groupDao.insertUserGroup(username, group)
    
    return r