from app.model.BaseModel import BaseModel


class StarItem(BaseModel):
    
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
