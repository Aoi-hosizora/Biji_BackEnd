class UserNotExistError(Exception):
    '''
    登录用户名未存在错误
    '''
    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return "User name \"%s\" not exist" % self.username