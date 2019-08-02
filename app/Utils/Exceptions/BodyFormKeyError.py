class BodyFormKeyError(Exception):
    '''
    请求 from-data 参数缺失或错误
    '''
    def __init__(self, keys=[]):
        self.keys = keys

    def __str__(self):
        if not len(self.keys) == 0:
            return "Body: form-data error, key %s not found or error" % list(self.keys)
        else:
            return "Body: form-data error."