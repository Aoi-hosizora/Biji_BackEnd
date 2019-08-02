class NoteExistError(Exception):
    '''
    笔记已存在错误
    '''
    def __init__(self, IdTitle: str):
        self.IdTitle = IdTitle

    def __str__(self):
        if isinstance(self.IdTitle, int):
            return "Note id: \"%d\" has existed" % self.IdTitle
        else:
            return "Note title: \"%s\" has existed" % self.IdTitle