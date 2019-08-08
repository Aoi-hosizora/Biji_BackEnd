from app.Config import Config

import redis
import json
import time

class TokenDAO(object):

    tbl_token = "tbl_token"

    def __init__(self):
        self.db = redis.Redis(
            host=Config.Redis_Host,
            port=Config.Redis_Port
        )
    
    def __del__(self):
        self.db.close()

    def addToken(self, token: str, username: str) -> bool:
        '''
        添加 token，默认过期时间是 Config.Def_Redis_Ex (s)
        '''
        self._removeExItem()
        return self.db.zadd(self.tbl_token, {
            json.dumps({
                'username': username,
                'token': token,
                'ct': time.time()
            }): Config.Def_Redis_Ex
        }) == 1

    def removeToken(self, username: str):
        '''
        删除用户 token
        '''
        allstr = self.db.zscan(self.tbl_token)[1]
        remlist = [
            objstr[0] for objstr in allstr 
            if json.loads(objstr[0])['username'] == username
        ]
        for rem in remlist:
            self.db.zrem(self.tbl_token, rem)
        self._removeExItem()

    def checkToken(self, token: str) -> [bool, bool]:
        '''
        判断是否存在 token
        先清除后返回结果：未过期但被清除 -> 重新插入

        @return 是否存在 是否即将被清除
        '''
        ret = False
        check = self._removeExItem(token)
        for objstr in self.db.zscan(self.tbl_token)[1]:
            s = json.loads(objstr[0])
            if s['token'] == token:
                ret = True
                break
        return ret, check

    def _removeExItem(self, checkToken: str="") -> bool:
        '''
        每对 Redis 操作都检查过期

        @return 需要检查的Token是否即将被删除
        '''
        allstr = self.db.zscan(self.tbl_token)[1]

        remlist = []
        ret = False
        for objstr in allstr:
            j = json.loads(objstr[0])
            if j['ct'] + objstr[1] < time.time():
                remlist.append(objstr[0])
                if checkToken != "" and j['token'] == checkToken:
                    ret = True

        # remlist = [
        #     objstr[0] for objstr in allstr
        #     if json.loads(objstr[0])['ct'] + objstr[1] < time.time()
        # ]
        # 老时间戳 + ex < 新时间戳
        for rem in remlist:
            self.db.zrem(self.tbl_token, rem)
        
        return ret
