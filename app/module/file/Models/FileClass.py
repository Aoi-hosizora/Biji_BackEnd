import datetime

class FileClass(object):
    def __init__(self, id: int, name: str):
        self.id: int = id
        self.name: str = name
    
    def toJson(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @staticmethod
    def toJsonSet(fileclasses):
        sets = []
        for fileclass in fileclasses:
            sets.append(fileclass.toJson())
        return sets