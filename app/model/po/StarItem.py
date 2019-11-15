from typing import Optional

from app.model.JsonModel import JsonModel


class StarItem(JsonModel):

    def __init__(self, sid: int, title, url, content):
        self.id: int = sid
        self.title: str = title
        self.url: str = url
        self.content: str = content

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'content': self.content
        }

    @staticmethod
    def from_json(jsonDict: dict) -> Optional:
        try:
            return StarItem(
                sid=jsonDict['id'],
                title=jsonDict['title'],
                url=jsonDict['url'],
                content=jsonDict['content']
            )
        except KeyError:
            return None
