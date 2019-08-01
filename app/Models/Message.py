class Message(object):

    def __init__(self, message: str, detail: str = ""):
        self.message = message
        self.detail = detail
    
    def toJson(self):
        if self.detail == "":
            return {
                'message': self.message
            }
        else:
            return {
                'message': self.message,
                'detail': self.detail
            }