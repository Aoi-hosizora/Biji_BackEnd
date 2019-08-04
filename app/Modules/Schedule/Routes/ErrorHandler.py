from app.Utils import RespUtil, ErrorUtil

from app.Modules.Schedule.Exceptions.ScheduleError import ScheduleError

def register_schedule_error_handler(error: TypeError):
    '''
    Schedule 模块的错误处理
    '''
    if isinstance(error, ScheduleError):
        return RespUtil.jsonRet(
            dict=ErrorUtil.getErrorMessageJson(error=error, title="Schedule Test Error"),
            code=ErrorUtil.BadRequest
        )
    else:
        return None