class InsertError(Exception):
    '''
    插入错误
    '''
    def __init__(self, username: str):
        self.user = username

    def __str__(self):
        return "Schedule of user \"%s\" insert error" % self.user
