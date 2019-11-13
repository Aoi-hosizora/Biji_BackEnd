class ExistError(Exception):
    '''
    已存在错误
    '''
    def __init__(self, IdTitle: str, isNote: bool=True):
        self.IdTitle = IdTitle
        self.isNote = isNote

    def __str__(self):
        if self.isNote:
            if isinstance(self.IdTitle, int):
                return "Note (id: %d) has existed" % self.IdTitle
            else:
                return "Note (title: \"%s\") has existed" % self.IdTitle
        else:
            if isinstance(self.IdTitle, int):
                return "Group (id: %d) has existed" % self.IdTitle
            else:
                return "Group (name: \"%s\") has existed" % self.IdTitle
