from app.config import Config

class UsernameFormatError(Exception):
    '''
    用户名格式错误
    '''
    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return "User name \"%s\" format error (should longer than or equals to %d and shorter then %d)" % (
            self.username, Config.UserNameMinLength, Config.UserNameMaxLength
        )