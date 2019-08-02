class DeleteError(Exception):
    '''
    删除错误
    '''
    def __init__(self, title: str):
        self.title = title

    def __str__(self):
        return "Star (title: \"%s\") delete error" % self.title