from app.Database.ScheduleDAO import ScheduleDAO

from app.Modules.Schedule.Models.Schedule import Schedule
from app.Modules.Schedule.Exceptions.ScheduleNotExistError import ScheduleNotExistError
from app.Modules.Schedule.Exceptions.InsertError import InsertError
from app.Modules.Schedule.Exceptions.DeleteError import DeleteError
from app.Modules.Schedule.Exceptions.UpdateError import UpdateError


def getSchedule(username: str) -> Schedule:
    '''
    查询课表
    '''
    scheduleDao = ScheduleDAO()
    ret = scheduleDao.querySchedule(username)
    if ret == None:
        raise ScheduleNotExistError(username)
    return ret


def insertSchedule(schedule: Schedule) -> bool:
    '''
    插入一个课表
    '''
    scheduleDao = ScheduleDAO()
    if scheduleDao.insertSchedule(schedule):
        return True
    else:
        raise InsertError(schedule.username)

def deleteSchedule(schedule: Schedule):
    '''
    删除一个课表
    '''
    scheduleDao = ScheduleDAO()
    if scheduleDao.deleteSchedule(schedule):
        return True
    else:
        raise DeleteError(schedule.username)

def updateSchedule(schedule: Schedule) -> bool:
    '''
    删除一个课表
    '''
    scheduleDao = ScheduleDAO()
    if scheduleDao.updateSchedule(schedule):
        return True
    else:
        raise UpdateError(schedule.username)