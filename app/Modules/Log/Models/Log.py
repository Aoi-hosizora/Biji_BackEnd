import datetime

class Log(object):

    def __init__(self, module: str, updateTime: datetime):
        self.module = module
        if isinstance(updateTime, datetime.datetime):
            self.updateTime = updateTime
        else:
            print(updateTime)
            self.updateTime = datetime.datetime.strptime(updateTime, "%Y-%m-%d %H:%M:%S") 
            print(type(self.updateTime))
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