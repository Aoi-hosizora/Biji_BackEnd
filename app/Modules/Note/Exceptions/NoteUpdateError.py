class NoteUpdateError(Exception):
    '''
    更新笔记错误
    '''
    def __init__(self, id: int):
        self.id = id

    def __str__(self):
        return "Note id: %d update error" % self.id