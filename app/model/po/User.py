from app.model.JsonModel import JsonModel


class User(JsonModel):

    def __init__(self, username: str, encrypted_pass: str):
        self.username = username
        self.encrypted_pass = encrypted_pass

    def to_json(self) -> dict:
        return {
            'username': self.username
        }
