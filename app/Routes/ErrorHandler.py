from app.Utils import ErrorUtil, RespUtil
from app.Models.Message import Message

from app.Routes.GlobalErrorHandle import register_global_error_handler
from app.Modules import Auth
from app.Modules import Note
from app.Modules import Star
from app.Modules import File
from app.Modules import Schedule
from app.Modules import Log

from flask.app import Flask

def register_error_forward(app: Flask):
    '''
    向 FlaskApp 添加错误转发，包括系统错误和模块内错误
    '''

    @app.errorhandler(404)
    def error_404(error: TypeError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Not Found"),
            code=ErrorUtil.NotFound
        )

    @app.errorhandler(405)
    def error_405(error: TypeError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Method Not Allowed"),
            code=ErrorUtil.MethodNotAllowed
        )

    @app.errorhandler(500)
    def error_500(error: TypeError):
        '''
        500 Error Forwarding
        '''

        err_glob = register_global_error_handler(error)
        err_auth = Auth.forward_auth_error(error)
        err_note = Note.forward_note_error(error)
        err_star = Star.forward_star_error(error)
        err_file = File.forward_file_error(error)
        err_schedule = Schedule.forward_schedule_error(error)
        err_log = Log.forward_log_error(error)

        if not err_glob == None:
            return err_glob
        elif not err_auth == None:
            return err_auth
        elif not err_note == None:
            return err_note
        elif not err_star == None:
            return err_star
        elif not err_file == None:
            return err_file
        elif not err_schedule == None:
            return err_schedule
        elif not err_log == None:
            return err_log
        else:
            return RespUtil.jsonRet(
                dict=ErrorUtil.getErrorMessageJson(error=error, title="Internal Server Error"),
                code=ErrorUtil.InternalServerError
            )
