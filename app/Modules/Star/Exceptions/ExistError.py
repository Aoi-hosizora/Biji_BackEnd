class ExistError(Exception):
    '''
    已存在错误
    '''
    def __init__(self, title: str):
        self.title = title

    def __str__(self):
        return "Star (title: \"%s\") has existed" % self.title
