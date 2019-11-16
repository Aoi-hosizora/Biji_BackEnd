from typing import Optional

from app.model.JsonModel import JsonModel
from app.model.po.DocumentClass import DocumentClass


class Document(JsonModel):

    def __init__(self, did: int, filename: str, docClass: DocumentClass, server_filename: str):
        self.id: int = did
        self.filename: str = filename  # 客户端文件名
        self.docClass: DocumentClass = docClass
        self.server_filename: str = server_filename  # 服务器存储文件名

    def to_json(self) -> dict:
        # 不序列化 filepath
        return {
            'id': self.id,
            'filename': self.filename,
            'docClass': self.docClass.to_json(),
            'server_filename': self.server_filename  # 服务器的文件名
        }

    @staticmethod
    def from_json(jsonDict: dict) -> Optional:
        try:
            # 不反序列化 filepath
            return Document(
                did=jsonDict['id'],
                filename=jsonDict['filename'],
                docClass=DocumentClass.from_json(jsonDict['docClass']),
                # server_filename=jsonDict['server_filename'],  # 插入 Document 时用
                server_filename=''
            )
        except KeyError:
            return None
