from app.config import Config

import redis


class ShareCodeDao(object):

    def __init__(self):
        self.db = redis.Redis(
            host=Config.Redis_Host,
            port=Config.Redis_Port
        )

    def __del__(self):
        self.db.close()

    def checkShareCode(self, key: str, value: str) -> bool:
        """
        检查share code是否过期和是否存在
        """
        return self.db.get(key) is not None

    def addShareCode(self, key: str, value: str) -> bool:
        """
        添加 share code，默认过期时间是 1h
        """
        self.db.set(key, value, ex=3600)
        if self.checkShareCode(key, value):
            return True
        else:
            return False
