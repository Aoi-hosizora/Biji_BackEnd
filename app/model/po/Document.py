from typing import Optional

from app.model.JsonModel import JsonModel


class Document(JsonModel):
    def __init__(self, uid: int, did: int, filename: str):
        self.uid: int = uid
        self.id: int = did
        self.filename: str = filename

    def to_json(self) -> dict:
        return {
            "user": self.uid,
            'id': self.id,
            'filename': self.filename
        }

    @staticmethod
    def from_json(jsonDict: dict) -> Optional:
        try:
            return Document(
                uid=jsonDict['user'],
                did=jsonDict['id'],
                filename=jsonDict['filename']
            )
        except KeyError:
            return None
