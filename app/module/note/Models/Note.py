from datetime import datetime

from app.module.note.Models import Group


class Note(object):
    def __init__(self, nid: int, title: str, content: str, group: Group, create_time: datetime, update_time: datetime):
        self.id = int(nid)
        self.title = title
        self.content = content
        self.group = group

        if isinstance(create_time, datetime):
            self.create_time = create_time
        else:
            self.create_time = datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')

        if isinstance(update_time, datetime):
            self.update_time = update_time
        else:
            self.update_time = datetime.strptime(update_time, '%Y-%m-%d %H:%M:%S')

    def toJson(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'group': self.group.toJson(),
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @staticmethod
    def toJsonSet(notes):
        sets = []
        for note in notes:
            sets.append(note.toJson())
        return sets