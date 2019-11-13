from app.model.JsonModel import JsonModel
from app.model.vo.ResultCode import ResultCode


class Result(JsonModel):
    """
    统一设置返回格式 状态码 信息 数据内容
    """

    def __init__(self):
        self.code: int = 200
        self.message: str = ''
        self.data: dict or list = {}
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

    def setData(self, obj: dict or list):
        self.data = obj
        return self

    def putData(self, name: str, data: dict):
        self.data[name] = data
        return self

    def to_json(self) -> dict:
        return {
            'code': self.code,
            'message': self.message,
            'data': self.data
        }
