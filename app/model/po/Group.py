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


Group.DEF_GROUP = Group(1, "默认分组", 0, '#F0F0F0')
