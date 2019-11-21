from app.model.JsonModel import JsonModel


class Group(JsonModel):

    def __init__(self, gid: int, name: str, order: int = -1, color: str = '#A5A5A5'):
        self.id: int = int(gid)
        self.name: str = name
        self.order: int = int(order)
        if not color or not color.startswith('#'):
            self.color: str = '#A5A5A5'
        else:
            self.color: str = color

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'order': self.order,
            'color': self.color
        }


DEF_GROUP = Group(1, "默认分组", 0, '#A5A5A5')
