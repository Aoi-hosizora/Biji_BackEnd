from app.database.ScheduleDAO import ScheduleDAO

from app.module.schedule.Models.Schedule import Schedule
from app.module.schedule.Exceptions.ScheduleNotExistError import ScheduleNotExistError
from app.module.schedule.Exceptions.InsertError import InsertError
from app.module.schedule.Exceptions.DeleteError import DeleteError
from app.module.schedule.Exceptions.UpdateError import UpdateError


def getSchedule(username: str) -> Schedule:
    '''
    查询课表
    '''
    scheduleDao = ScheduleDAO()
    ret = scheduleDao.querySchedule(username)
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