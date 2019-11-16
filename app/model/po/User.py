from app.model.JsonModel import JsonModel


class User(JsonModel):

    def __init__(self, uid: int, username: str, encrypted_pass: str):
        self.id: int = int(uid)
        self.username: str = username
        self.encrypted_pass: str = encrypted_pass

    def to_json(self) -> dict:
        return {
            "id": self.id,
            'username': self.username
        }
