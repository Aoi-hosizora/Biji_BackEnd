class File(object):
    def __init__(self, username: str, foldername: str, filename: str, filepath: str):
        self.username = username
        self.foldername = foldername
        self.filename = filename
        self.filepath = filepath

    def toJson(self):
        return {
            'foldername': self.foldername,
            'filename': self.filename,
        }

    @staticmethod
    def toJsonSet(files):
        sets = []
        for file in files:
            sets.append(file.toJson())
        return sets