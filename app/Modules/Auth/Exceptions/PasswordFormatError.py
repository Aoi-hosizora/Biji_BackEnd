from app.Config import Config

class PasswordFormatError(Exception):
    '''
    密码格式错误
    '''
    def __init__(self):
        pass

    def __str__(self):
        return "Password format error (should longer than or equals to %d and shorter then %d)" % (
            Config.PassWordMinLength, Config.PassWordMaxLength
        )