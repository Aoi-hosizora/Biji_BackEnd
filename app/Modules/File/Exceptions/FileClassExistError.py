class FileClassExistError(Exception):
    '''
    已存在错误
    '''
    def __init__(self, fileClassName: str):
        self.fileClassName = fileClassName

    def __str__(self):
        return "FileClass (name: \"%s\") has existed" % self.fileClassName
