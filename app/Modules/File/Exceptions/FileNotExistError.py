class FileNotExistError(Exception):
    '''
    文件不存在
    '''
    def __init__(self, filename: str = ""):
        self.filename = filename

    def __str__(self):
        return "File \"%s\" not exist" % self.filename