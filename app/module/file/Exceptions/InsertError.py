class InsertError(Exception):
    '''
    插入错误
    '''
    def __init__(self, name: str, isfile: bool = True):
        self.name = name
        self.isfile = isfile

    def __str__(self):
        if self.isfile:
            return "File \"%s\" insert error" % self.name
        return "FileClass \"%s\" insert error" % self.name
