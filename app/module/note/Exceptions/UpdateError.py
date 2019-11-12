class UpdateError(Exception):
    '''
    更新错误
    '''
    def __init__(self, id: int, isNote: bool=True):
        self.id = id
        self.isNote = isNote

    def __str__(self):
        if self.isNote:
            return "Note (title: \"%s\") update error" % self.title
        else:
            return "Group (name: \"%s\") update error" % self.title