class LoginPasswordError(Exception):
    '''
    密码错误
    '''
    def __init__(self, username: str = ""):
        self.username = username

    def __str__(self):
        if self.username == "":
            return "User password error"
        else:
            return "User \"%s\" password error" % self.username
