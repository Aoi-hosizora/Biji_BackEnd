from datetime import datetime
from typing import Optional

from app.model.JsonModel import JsonModel
from app.model.po.Group import Group


class Note(JsonModel):

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

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'group': self.group.to_json(),
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    @staticmethod
    def from_json(jsonDict: dict) -> Optional:
        try:
            return Note(
                nid=jsonDict['id'],
                title=jsonDict['title'],
                content=jsonDict['content'],
                group=Group.from_json(jsonDict['group']),
                create_time=jsonDict['create_time'],
                update_time=jsonDict['update_time']
            )
        except KeyError:
            return None
