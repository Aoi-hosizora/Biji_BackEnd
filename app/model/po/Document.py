from typing import Union

from app.model.JsonModel import JsonModel
from app.model.po.DocClass import DocClass


class Document(JsonModel):

    def __init__(self, did: int, filename: str, docClass: Union[DocClass, int], uuid: str = ''):
        self.id: int = int(did)
        self.filename: str = filename  # 客户端文件名
        self.uuid: str = uuid  # 服务器存储文件名，更新不会用到
        if isinstance(docClass, DocClass):
            self.docClass: DocClass = docClass
        else:
            self.docClass: DocClass = DocClass(cid=int(docClass), name='')

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'filename': self.filename,
            'docClass': self.docClass.to_json(),
            'uuid': self.uuid
        }
