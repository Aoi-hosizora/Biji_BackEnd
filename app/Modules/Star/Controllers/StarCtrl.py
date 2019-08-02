from app.Database.StarDAO import StarDAO
from app.Utils.Exceptions.BodyRawJsonError import BodyRawJsonError

from app.Modules.Star.Models.StarItem import StarItem
from app.Modules.Star.Exceptions.InsertError import InsertError
from app.Modules.Star.Exceptions.DeleteError import DeleteError

import json

def getStarFromReqData(reqdata: str) -> StarItem:
    '''
    从 Req 的 headers 中获取 Star

    `getStarFromReqData(request.headers)`
    '''
    try:
        postjson = json.loads(reqdata)
    except:
        # 解析错误
        raise BodyRawJsonError()

    keys = ['title', 'url', 'content']
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
        return StarItem(*[postjson[key] for key in keys])
    except:
        # 内容错误
        raise BodyRawJsonError()

def getAllStars(username: str) -> [StarItem]:
    '''
    查询所有收藏
    '''
    starDao = StarDAO()
    return starDao.queryUserAllStars(username)

def insertStar(username: str, star: StarItem) -> bool:
    '''
    插入一个新收藏
    '''
    starDao = StarDAO()
    if starDao.insertUserStar(username, star):
        return True
    else:
        raise InsertError(star.title)

def deleteStar(username: str, star: StarItem) -> bool:
    '''
    删除一个旧收藏
    '''
    starDao = StarDAO()
    if starDao.deleteUserStar(username, star):
        return True
    else:
        raise DeleteError(star.title)
