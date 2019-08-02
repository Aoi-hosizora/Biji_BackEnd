class InsertError(Exception):
    '''
    插入错误
    '''
    def __init__(self, title: str):
        self.title = title

    def __str__(self):
        return "Star (title: \"%s\") insert error" % self.title