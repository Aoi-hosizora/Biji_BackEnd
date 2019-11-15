from flask import Response, make_response

from app.model.dto.ResultCode import ResultCode


class RawResult(object):
    """
    统一设置返回格式 二进制数据 (图片，文件)
    """

    def __init__(self, code: int = 200, data: bytes = None):
        self.code: int = code
        self.data: bytes = data

    @staticmethod
    def ok():
        """
        成功返回数据
        """
        return RawResult(code=ResultCode.SUCCESS.code)

    @staticmethod
    def error(err: ResultCode = ResultCode.INTERNAL_SERVER_ERROR):
        """ 错误码返回数据 """
        return RawResult(code=err.code)

    def setCode(self, code: int):
        """ 链式设置响应状态码 """
        self.code = code
        return self

    def setData(self, data: bytes):
        """ 链式设置返回数据 """
        self.data = data
        return self

    def raw_ret(self, headers=None, is_image=True) -> Response:
        """ 自定义二进制数据返回 Response """
        if headers is None:
            headers = {}

        resp = make_response(self.data)

        resp.status_code = self.code
        resp.headers['Access-Control-Allow-Origin'] = '*'
        if is_image:
            resp.headers['Content-Type'] = 'image/png'
        for k, v in headers.items():
            resp.headers[k] = v

        return resp
