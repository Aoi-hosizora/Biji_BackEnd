import traceback
from flask.app import Flask

from app.model.dto.ResultCode import ResultCode
from app.model.dto.Result import Result
from itsdangerous import SignatureExpired, BadSignature

from app.route.ParamType import ParamError, ParamType


def setup_error_forward(app: Flask):
    """
    向 FlaskApp 注册 系统错误转发
    """

    @app.errorhandler(400)
    def error_400(error: TypeError):
        return Result.error(ResultCode.BAD_REQUEST).setMessage(str(error)).json_ret()

    @app.errorhandler(401)
    def error_401(error: TypeError):
        return Result.error(ResultCode.UNAUTHORIZED).setMessage(str(error)).json_ret()

    @app.errorhandler(403)
    def error_403(error: TypeError):
        return Result.error(ResultCode.FORBIDDEN).setMessage(str(error)).json_ret()

    @app.errorhandler(404)
    def error_404(error: TypeError):
        return Result.error(ResultCode.NOT_FOUND).setMessage(str(error)).json_ret()

    @app.errorhandler(405)
    def error_405(error: TypeError):
        return Result.error(ResultCode.METHOD_NOT_ALLOWED).setMessage(str(error)).json_ret()

    @app.errorhandler(406)
    def error_406(error: TypeError):
        return Result.error(ResultCode.NOT_ACCEPTABLE).setMessage(str(error)).json_ret()

    @app.errorhandler(500)
    def error_500(error: TypeError):
        return Result.error(ResultCode.INTERNAL_SERVER_ERROR).setMessage(str(error) + ': ' + traceback.format_exc()).json_ret()  # 500

    @app.errorhandler(Exception)
    def error_exception(error: TypeError):
        """
        500 Error Forwarding
        """
        print('error_exception: ', error)
        print(traceback.format_exc())

        if isinstance(error, BadSignature):
            return Result.error(ResultCode.UNAUTHORIZED).setMessage("Token Bad Signature").setData(str(error)).json_ret()  # 401
        if isinstance(error, SignatureExpired):
            return Result.error(ResultCode.UNAUTHORIZED).setMessage("Token Expired").setData(str(error)).json_ret()  # 401
        if isinstance(error, ParamError):
            message = 'Request Query Param Error' if error.paramType == ParamType.QUERY else \
                      'Request Route Param Error' if error.paramType == ParamType.ROUTE else \
                      'Request Route Param Error' if error.paramType == ParamType.FORM else \
                      'Request Form Data Param Error' if error.paramType == ParamType.RAW else \
                      'Request Raw Json Param Error'
            return Result.error(ResultCode.BAD_REQUEST).setMessage(message).json_ret()  # 400

        return Result.error(ResultCode.INTERNAL_SERVER_ERROR).setMessage(str(error)).json_ret()  # 500
