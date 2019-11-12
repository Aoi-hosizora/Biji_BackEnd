class Schedule(object):
    def __init__(self, username: str, schedulejson: str):
        self.username = username
        self.schedulejson = schedulejson

    def toJson(self):
        return {
            'schedulejson': self.schedulejson
        }

    @staticmethod
    def toJsonSet(schedules):
        sets = []
        for schedule in schedules:
            sets.append(schedule.toJson())
        return sets