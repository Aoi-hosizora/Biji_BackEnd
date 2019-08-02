class NoteDeleteError(Exception):
    '''
    删除笔记错误
    '''
    def __init__(self, title: str):
        self.title = title

    def __str__(self):
        return "Note title: \"%s\" delete error" % self.title