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

    def addToken(self, token: str, username: str, ex: int) -> bool:
        '''
        添加 token
        '''
        self._removeExItem()
        return self.db.zadd(self.tbl_token, {
            json.dumps({
                'username': username,
                'token': token,
                'ct': time.time()
            }): ex
        }) == 1

    def removeToken(self, username: str) -> bool:
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

    def checkToken(self, token: str) -> bool:
        self._removeExItem()
        for objstr in self.db.zscan(self.tbl_token)[1]:
            s = json.loads(objstr[0])
            if s['token'] == token:
                return True
        return False

    def _removeExItem(self):
        '''
        每对 Redis 操作都检查过期
        '''
        allstr = self.db.zscan(self.tbl_token)[1]
        remlist = [
            objstr[0] for objstr in allstr 
            if json.loads(objstr[0])['ct'] + objstr[1] < time.time()
        ]
        # 老时间戳 + ex < 新时间戳
        for rem in remlist:
            self.db.zrem(self.tbl_token, rem)
