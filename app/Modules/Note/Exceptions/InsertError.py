class InsertError(Exception):
    '''
    插入错误
    '''
    def __init__(self, title: str, isNote: bool=True):
        self.title = title
        self.isNote = isNote

    def __str__(self):
        if self.isNote:
            return "Note (title: \"%s\") insert error" % self.title
        else:
            return "Group (name: \"%s\") insert error" % self.title