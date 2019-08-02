class NotExistError(Exception):
    '''
    不存在错误
    '''
    def __init__(self, title: str):
        self.title = title

    def __str__(self):
        return "Star (title: \"%s\") not exist" % self.title
