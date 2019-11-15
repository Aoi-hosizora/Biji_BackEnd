from app.model.JsonModel import JsonModel


class User(JsonModel):

    def __init__(self, uid: int, username: str, encrypted_pass: str):
        self.id = uid
        self.username = username
        self.encrypted_pass = encrypted_pass

    def to_json(self) -> dict:
        return {
            "id": self.id,
            'username': self.username
        }

    # No from_json
