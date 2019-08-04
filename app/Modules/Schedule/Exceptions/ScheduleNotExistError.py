class ScheduleNotExistError(Exception):
    '''
    课表不存在
    '''
    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return "Schedule of user \"%s\" not exist" % self.username