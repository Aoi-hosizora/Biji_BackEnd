from typing import Optional

from app.model.JsonModel import JsonModel
from app.model.po.DocumentClass import DocumentClass


class Document(JsonModel):

    def __init__(self, did: int, filename: str, docClass: DocumentClass):
        self.id: int = did
        self.filename: str = filename
        self.docClass: DocumentClass = docClass

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'filename': self.filename,
            'docClass': self.docClass.to_json()
        }

    @staticmethod
    def from_json(jsonDict: dict) -> Optional:
        try:
            return Document(
                did=jsonDict['id'],
                filename=jsonDict['filename'],
                docClass=DocumentClass.from_json(jsonDict['docClass'])
            )
        except KeyError:
            return None
