class NoteNotExistError(Exception):
    '''
    查询笔记不存在错误
    '''
    def __init__(self, IdTitle: int):
        self.IdTitle = IdTitle

    def __str__(self):
        if isinstance(self.IdTitle, int):
            return "Note id: %d not exist" % self.IdTitle
        else:
            return "Note title: %s not exist" % self.IdTitle