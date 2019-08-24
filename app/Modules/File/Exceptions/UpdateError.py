class UpdateError(Exception):
    '''
    更新错误
    '''
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return "FileClass (name: \"%s\") update error" % self.name
