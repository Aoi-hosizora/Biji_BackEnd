class BodyRawJsonError(Exception):
    '''
    请求 raw-Json 缺失或错误
    '''
    def __init__(self, keys=[]):
        self.keys = keys

    def __str__(self):
        if not len(self.keys) == 0:
            return "Body: json key-value error, key %s not found or error" % list(self.keys)
        else:
            return "Body: json key-value error."