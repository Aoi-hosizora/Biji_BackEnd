class DeleteError(Exception):
    '''
    删除错误
    '''
    def __init__(self, name: str, isfile: bool = True):
        self.name = name
        self.isfile = isfile

    def __str__(self):
        if self.isfile:
            return "File \"%s\" delete error" % self.name
        return "FileClass \"%s\" delete error" % self.name
