import json

from app.database.RedisHelper import RedisHelper


class UserTokenDao(RedisHelper):
    ssn_name = 'ssn_token'

    def __init__(self):
        super(UserTokenDao, self).__init__()

    def addToken(self, uid: int, token: str) -> bool:
        """
        添加 Token 不删除原有 Token (允许同时多登录)
        :return: 是否创建成功
        """
        count = self.db.sadd(
            self.ssn_name,
            json.dumps({'uid': uid, 'token': token})
        )
        return count != 0

    def checkToken(self, token: str) -> bool:
        """
        判断 Token 是否存在
        """
        for jsonStr in self.db.sinter(self.ssn_name):
            if json.loads(jsonStr).get('token') == token:
                return True
        return False

    def removeToken(self, uid: int) -> int:
        """
        移除用户所有 Token
        :return: 移除的 Token 数
        """
        remList = [
            jsonStr for jsonStr in self.db.sinter(self.ssn_name)
            if json.loads(jsonStr).get('uid') == uid
        ]
        count = self.db.srem(self.ssn_name, *remList)
        return count
