from datetime import datetime
from typing import Union

from app.model.JsonModel import JsonModel
from app.model.po.Group import Group


class Note(JsonModel):

    def __init__(self, nid: int, title: str, content: str, group: Union[Group, int], create_time: datetime = '', update_time: datetime = ''):
        self.id: int = int(nid)
        self.title: str = title
        self.content: str = content
        if isinstance(group, Group):
            self.group: Group = group
        else:
            self.group: Group = Group(group, '', -1, '')

        if isinstance(create_time, datetime):
            self.create_time = create_time
        else:
            try:
                self.create_time = datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                self.create_time = datetime.now()

        if isinstance(update_time, datetime):
            self.update_time = update_time
        else:
            try:
                self.update_time = datetime.strptime(update_time, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                self.update_time = datetime.now()

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'group': self.group.to_json(),
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }
