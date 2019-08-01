class UserExistError(Exception):
    '''
    注册用户名已经存在错误
    '''
    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return "Registered user name \"%s\" has existed" % self.username