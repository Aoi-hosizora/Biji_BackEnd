class DeleteError(Exception):
    '''
    删除错误
    '''
    def __init__(self, username: str):
        self.user = username

    def __str__(self):
        return "Schedule of user \"%s\" delete error" % self.user
