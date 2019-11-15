import json
from typing import List, Union

from flask import Response

from app.model.JsonModel import JsonModel
from app.model.dto.ResultCode import ResultCode


class Result(JsonModel):
    """
    统一设置返回格式 状态码 信息 数据内容
    """

    def __init__(self, code: int = 200, message: str = '', data=None):
        if data is None:
            data = {}

        self.code = code
        self.message = message
        self.data = data  # 默认 字典，可为: 字典 / 列表 / 字符串
        pass

    @staticmethod
    def ok():
        """
        成功相应处理
        """
        return Result(code=ResultCode.SUCCESS.code, message=ResultCode.SUCCESS.message)

    @staticmethod
    def error(err: ResultCode = ResultCode.INTERNAL_SERVER_ERROR):
        """
        错误相应处理
        """
        return Result(code=err.code, message=err.message)

    def setCode(self, code: int):
        """
        链式设置响应状态码
        """
        self.code = code
        return self

    def setMessage(self, message: str):
        """
        链式设置响应信息
        """
        self.message = message
        return self

    def setData(self, obj: Union[dict, List[dict], str]):
        """
        直接设置 字典 列表 字符串
        """
        self.data = obj
        return self

    def putData(self, name: str, data: Union[dict, str, int, float, list]):
        """
        添加进字典
        """
        self.data[name] = data
        return self

    def to_json(self) -> dict:
        return {
            'code': self.code,
            'message': self.message,
            'data': self.data
        }

    def json_ret(self, headers=None) -> Response:
        """
        Flask 自定义数据返回
        """
        if headers is None:
            headers = {}

        resp = Response(
            response=json.dumps(obj=self.to_json(), indent=4, ensure_ascii=False).encode("utf-8"),
            mimetype='application/json'
        )
        resp.status_code = self.code
        resp.headers['Access-Control-Allow-Origin'] = '*'
        for k, v in headers.items():
            resp.headers[k] = v

        return resp
