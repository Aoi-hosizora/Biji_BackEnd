class File(object):
    def __init__(self, username: str, id: int, foldername: str, filename: str, filepath: str):
        self.username = username
        self.id = id
        self.foldername = foldername
        self.filename = filename
        self.filepath = filepath

    def toJson(self):
        return {
            'id': self.id,
            'foldername': self.foldername,
            'filename': self.filename,
        }

    @staticmethod
    def toJsonSet(files):
        sets = []
        for file in files:
            sets.append(file.toJson())
        return sets