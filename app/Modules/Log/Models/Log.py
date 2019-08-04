import datetime

class Log(object):

    def __init__(self, module: str, updateTime: datetime):
        self.module = module
        self.updateTime = updateTime

    def toJson(self):
        return {
            'module': self.module,
            'ut': self.updateTime.strftime('%Y-%m-%d %H:%M:%S')
        }

    @staticmethod
    def toJsonSet(logs):
        sets = []
        for log in logs:
            sets.append(log.toJson())
        return sets