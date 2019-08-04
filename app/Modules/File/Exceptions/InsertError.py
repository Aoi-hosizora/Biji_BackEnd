class InsertError(Exception):
    '''
    插入错误
    '''
    def __init__(self, filename: str):
        self.file = filename

    def __str__(self):
        return "File \"%s\" insert error" % self.file