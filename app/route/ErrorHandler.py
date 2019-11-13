from app.util import ErrorUtil, RespUtil

from app.route.GlobalErrorHandle import register_global_error_handler
from app.module import auth
from app.module import note
from app.module import star
from app.module import file
from app.module import schedule
from app.module import log

from flask.app import Flask


def register_error_forward(app: Flask):
    """
    向 FlaskApp 添加错误转发，包括系统错误和模块内错误
    """

    @app.errorhandler(404)
    def error_404(error: TypeError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Not Found"),
            code=ErrorUtil.NotFound
        )

    @app.errorhandler(405)
    def error_405(error: TypeError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Method Not Allowed"),
            code=ErrorUtil.MethodNotAllowed
        )

    @app.errorhandler(500)
    def error_500(error: TypeError):
        """
        500 Error Forwarding
        """

        err_glob = register_global_error_handler(error)
        err_auth = auth.forward_auth_error(error)
        err_note = note.forward_note_error(error)
        err_star = star.forward_star_error(error)
        err_file = file.forward_file_error(error)
        err_schedule = schedule.forward_schedule_error(error)
        err_log = log.forward_log_error(error)

        if err_glob is not None:
            return err_glob
        elif err_auth is not None:
            return err_auth
        elif err_note is not None:
            return err_note
        elif err_star is not None:
            return err_star
        elif err_file is not None:
            return err_file
        elif err_schedule is not None:
            return err_schedule
        elif err_log is not None:
            return err_log
        else:
            return RespUtil.jsonRet(
                data=ErrorUtil.getErrorMessageJson(error=error, title="Internal Server Error"),
                code=ErrorUtil.InternalServerError
            )