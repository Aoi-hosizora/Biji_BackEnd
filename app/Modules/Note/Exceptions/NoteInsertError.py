class NoteInsertError(Exception):
    '''
    插入笔记错误
    '''
    def __init__(self, title: str):
        self.title = title

    def __str__(self):
        return "Note title: \"%s\" insert error" % self.title