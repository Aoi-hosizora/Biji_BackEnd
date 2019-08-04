class ExistError(Exception):
    '''
    已存在错误
    '''
    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return "Schedule of user \"%s\" has existed" % self.username
