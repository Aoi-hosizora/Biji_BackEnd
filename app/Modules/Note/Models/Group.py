import datetime

class Group(object):
    def __init__(self, id: int, name: str, order: int, color: str):
        self.id = id
        self.name = name
        self.order = order
        self.color = color
    
    def toJson(self):
        return {
            'id': self.id,
            'name': self.name,
            'order': self.order,
            'color': self.color
        }