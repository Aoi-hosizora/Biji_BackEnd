class LogoutError(Exception):
    '''
    注销错误
    '''
    def __init__(self, username: str):
        self.username = username
        pass

    def __str__(self):
        return "User \"%s\" logout error" % self.username
