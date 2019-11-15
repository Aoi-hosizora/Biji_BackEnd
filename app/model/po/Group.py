from typing import Optional

from app.model.JsonModel import JsonModel


class Group(JsonModel):

    def __init__(self, gid: int, name: str, order: int, color: str):
        self.id = int(gid)
        self.name = name
        self.order = int(order)
        self.color = color

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'order': self.order,
            'color': self.color
        }

    @staticmethod
    def from_json(jsonDict: dict) -> Optional:
        try:
            return Group(
                gid=jsonDict['id'],
                name=jsonDict['name'],
                order=jsonDict['order'],
                color=jsonDict['color']
            )
        except KeyError:
            return None


DEF_GROUP = Group(1, "默认分组", 0, '#F0F0F0')
