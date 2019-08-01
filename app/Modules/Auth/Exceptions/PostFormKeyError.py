class PostFormKeyError(Exception):
    '''
    POST 请求参数缺失或错误
    '''
    def __init__(self, keys=[]):
        self.keys = keys

    def __str__(self):
        if not len(self.keys) == 0:
            return "Post form-data error, key %s not found or null" % self.keys
        else:
            return "Post form-data error."