class FileTypeError(Exception):
    '''
    文件类型错误
    '''
    def __init__(self, ext: str = ""):
        self.ext = ext

    def __str__(self):
        return "File type \"%s\" not supported" % self.ext