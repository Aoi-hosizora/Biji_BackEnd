class ExistError(Exception):
    '''
    已存在错误
    '''
    def __init__(self, foldername: str, filename: str):
        self.folder = foldername
        self.file = filename

    def __str__(self):
        return "File \"%s\" in folder \"%s\" has existed" % (self.file, self.folder)
