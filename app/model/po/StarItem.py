from app.model.JsonModel import JsonModel


class StarItem(JsonModel):

    def __init__(self, sid: int, title: str, url: str, content: str):
        self.id: int = int(sid)
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
