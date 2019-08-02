class AuthNoneError(Exception):
    '''
    认证错误，不存在认证头
    '''
    def __init__(self):
        pass

    def __str__(self):
        return "Header \"Authorization\" not found"
