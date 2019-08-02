import datetime

class Note(object):
    def __init__(self, id: int, title: str, content: str, group_id: str, create_time: datetime, update_time: datetime):
        self.id = id
        self.title = title
        self.content = content
        self.group_id = group_id
        self.create_time = create_time
        self.update_time = update_time
    
    def toJson(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'group_id': self.group_id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @staticmethod
    def toJsonSet(notes):
        sets = []
        for note in notes:
            sets.append(note.toJson())
        return sets