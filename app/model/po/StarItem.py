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
