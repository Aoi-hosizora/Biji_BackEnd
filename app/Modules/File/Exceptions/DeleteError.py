class DeleteError(Exception):
    '''
    删除错误
    '''
    def __init__(self, filename: str):
        self.file = filename

    def __str__(self):
        return "File \"%s\" delete error" % self.file
