class RegLogInfo(object):
    '''
    登录注册返回信息
    
    @return `username` `status`
    '''
    def __init__(self, username: str, isLogin: bool):
        self.username = username
        self.isLogin = isLogin
    
    def toJson(self):
        status = 'Login Success' if self.isLogin else 'Register Success'
        return {
            'username': self.username,
            'status': status
        }