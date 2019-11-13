class UpdateError(Exception):
    '''
    课表更新错误
    '''
    def __init__(self, username: str):
        self.user = username

    def __str__(self):
        return "Schedule of user \"%s\" update error" % self.user
