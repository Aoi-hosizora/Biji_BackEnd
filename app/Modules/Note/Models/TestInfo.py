class TestInfo(object):
    def __init__(self, msg: str):
        self.msg = msg
    
    def toJson(self):
        return {
            'msg': self.msg
        }