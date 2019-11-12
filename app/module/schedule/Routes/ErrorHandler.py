from app.util import RespUtil, ErrorUtil

from app.module.schedule.Exceptions.ScheduleError import ScheduleError

def register_schedule_error_handler(error: TypeError):
    '''
    Schedule 模块的错误处理
    '''
    if isinstance(error, ScheduleError):
        return RespUtil.jsonRet(
            data=ErrorUtil.getErrorMessageJson(error=error, title="Schedule Test Error"),
            code=ErrorUtil.BadRequest
        )
    else:
        return None