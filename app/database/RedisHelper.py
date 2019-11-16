import redis

from app.config.Config import Config


class RedisHelper(object):

    def __init__(self):
        self.db = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT
        )

    def __del__(self):
        self.db.close()
