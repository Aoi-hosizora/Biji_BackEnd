from typing import Optional

from app.model.JsonModel import JsonModel


class StarItem(JsonModel):

    def __init__(self, title, url, content):
        self.title = title
        self.url = url
        self.content = content

    def to_json(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content
        }

    @staticmethod
    def from_json(jsonDict: dict) -> Optional:
        try:
            return StarItem(
                title=jsonDict['title'],
                url=jsonDict['url'],
                content=jsonDict['content']
            )
        except KeyError:
            return None
