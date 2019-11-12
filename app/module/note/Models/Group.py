import datetime

class Group(object):
    def __init__(self, id: int, name: str, order: int, color: str):
        self.id = int(id)
        self.name = name
        self.order = int(order)
        self.color = color
    
    def toJson(self):
        return {
            'id': self.id,
            'name': self.name,
            'order': self.order,
            'color': self.color
        }
    
    @staticmethod
    def toJsonSet(groups):
        sets = []
        for note in groups:
            sets.append(note.toJson())
        return sets