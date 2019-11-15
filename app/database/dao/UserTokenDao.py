import json

from app.database.RedisHelper import RedisHelper


class UserTokenDao(RedisHelper):
    ssn_name = 'ssn_token'

    def __init__(self):
        super().__init__()

    def addToken(self, uid: int, token: str) -> bool:
        """
        添加 Token 不删除原有 Token (允许同时多登录)
        :return: 是否创建成功
        """
        count = self.db.zadd(self.ssn_name, {
            json.dumps({
                'uid': uid,
                'token': token
            })
        })
        return count != 0

    def checkToken(self, token: str) -> bool:
        """
        判断 Token 是否存在
        """
        for jsonStr in self.db.zscan(self.ssn_name)[1]:
            if json.loads(jsonStr[0])['token'] == token:
                return True
        return False

    def removeToken(self, uid: int) -> int:
        """
        移除用户所有 Token
        :return: 移除的 Token 数
        """
        allJson = self.db.zscan(self.ssn_name)[1]
        remList = [
            jsonStr[0] for jsonStr in allJson
            if json.loads(jsonStr[0])['uid'] == uid
        ]
        count = 0
        for rem in remList:
            count += self.db.zrem(self.ssn_name, rem)
        return count
