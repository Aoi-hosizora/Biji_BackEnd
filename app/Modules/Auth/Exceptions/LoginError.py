class LoginError(Exception):
    '''
    登录密码错误
    '''
    def __init__(self, username: str = ""):
        self.username = username

    def __str__(self):
        if self.username == "":
            return "User login error"
        else:
            return "User \"%s\" login error" % self.username
