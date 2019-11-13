class RegisterError(Exception):
    '''
    注册用户名错误
    '''
    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return "User name \"%s\" register error" % self.username