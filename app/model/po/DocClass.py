from app.model.JsonModel import JsonModel


class DocClass(JsonModel):

    def __init__(self, cid: int, name: str):
        self.id: int = int(cid)
        self.name: str = str(name)

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }


DEF_DOC_CLASS = DocClass(1, "默认分组")
