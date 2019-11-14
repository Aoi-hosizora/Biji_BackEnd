from flask.app import Flask

from app.model.vo.ResultCode import ResultCode
from app.model.vo.Result import Result
from itsdangerous import SignatureExpired, BadSignature

from app.route.ParamError import ParamError, ParamType


def setup_error_forward(app: Flask):
    """
    向 FlaskApp 注册 系统错误转发
    """

    @app.errorhandler(404)
    def error_404():
        return Result.error(ResultCode.NOT_FOUND)

    @app.errorhandler(403)
    def error_404():
        return Result.error(ResultCode.FORBIDDEN)

    @app.errorhandler(405)
    def error_404():
        return Result.error(ResultCode.METHOD_NOT_ALLOWED)

    @app.errorhandler(500)
    def error_500(error: TypeError):
        """
        500 Error Forwarding
        """
        if isinstance(error, SignatureExpired):
            return Result.error(ResultCode.UNAUTHORIZED).setMessage("Token Expired")  # 401
        if isinstance(error, BadSignature):
            return Result.error(ResultCode.UNAUTHORIZED).setMessage("Token Bad Signature")  # 401

        if isinstance(error, ParamError):
            message = 'Request Query Param Error' if error.paramType == ParamType.QUERY else \
                      'Request Route Param Error' if error.paramType == ParamType.ROUTE else \
                      'Request Route Param Error' if error.paramType == ParamType.FORM else \
                      'Request Form Data Param Error' if error.paramType == ParamType.RAW else \
                      'Request Raw Json Param Error'
            return Result.error(ResultCode.NOT_ACCEPTABLE).setMessage(message)  # 406

        return Result.error(ResultCode.INTERNAL_SERVER_ERROR)  # 500
