from app.model.ResultCode import ResultCode


class Result(object):

    def __init__(self):
        self.code: int = 200
        self.message: str = ''
        self.data = {}
        pass

    @staticmethod
    def setResult(code: ResultCode):
        r = Result()
        r.code = code.code
        r.message = code.message
        return r

    @staticmethod
    def ok():
        return Result.setResult(ResultCode.SUCCESS)

    @staticmethod
    def error():
        return Result.setResult(ResultCode.INTERNAL_SERVER_ERROR)

    def setCode(self, code: int):
        self.code = code
        return self

    def setMessage(self, message: str):
        self.message = message
        return self

    def setData(self, obj):
        self.data = obj
        return self
