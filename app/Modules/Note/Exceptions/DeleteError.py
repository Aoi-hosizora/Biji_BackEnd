class DeleteError(Exception):
    '''
    删除错误
    '''
    def __init__(self, title: str, isNote: bool=True):
        self.title = title
        self.isNote = isNote

    def __str__(self):
        if self.isNote:
            return "Note (title: \"%s\") delete error" % self.title
        else:
            return "Group (name: \"%s\") delete error" % self.title