from typing import Optional

from app.model.JsonModel import JsonModel


class DocumentClass(JsonModel):

    def __init__(self, cid: int, name: str):
        self.id: int = cid
        self.name: str = name

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }

    @staticmethod
    def from_json(jsonDict: dict) -> Optional:
        try:
            return DocumentClass(
                cid=jsonDict['id'],
                name=jsonDict['name']
            )
        except KeyError:
            return None


DEF_DOC_CLASS = DocumentClass(1, "默认分组")
