class NotExistError(Exception):
    '''
    不存在错误
    '''
    def __init__(self, IdTitle: str, isNote: bool=True):
        self.IdTitle = IdTitle
        self.isNote = isNote

    def __str__(self):
        if self.isNote:
            if isinstance(self.IdTitle, int):
                return "Note (id: %d) not exist" % self.IdTitle
            else:
                return "Note (title: \"%s\") not exist" % self.IdTitle
        else:
            if isinstance(self.IdTitle, int):
                return "Group (id: %d) not exist" % self.IdTitle
            else:
                return "Group (name: \"%s\") not exist" % self.IdTitle
