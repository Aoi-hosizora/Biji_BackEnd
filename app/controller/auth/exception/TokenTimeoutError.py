class TokenTimeoutError(Exception):
    '''
    登录过期错误
    '''
    def __init__(self):
        pass

    def __str__(self):
        return "User login timeout"