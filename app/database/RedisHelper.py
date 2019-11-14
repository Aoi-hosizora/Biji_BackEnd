import redis

from app.config import Config


class RedisHelper(object):

    def __init__(self):
        self.db = redis.Redis(
            host=Config.Redis_Host,
            port=Config.Redis_Port
        )

    def __del__(self):
        self.db.close()
