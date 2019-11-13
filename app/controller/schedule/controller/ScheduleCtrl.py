from app.database.dao.ScheduleDao import ScheduleDao

from app.model.po.Schedule import Schedule
from app.controller.schedule.exception.InsertError import InsertError
from app.controller.schedule.exception.DeleteError import DeleteError
from app.controller.schedule.exception.UpdateError import UpdateError


def getSchedule(username: str) -> Schedule:
    '''
    查询课表
    '''
    scheduleDao = ScheduleDao()
    ret = scheduleDao.querySchedule(username)
    return ret


def insertSchedule(schedule: Schedule) -> bool:
    '''
    插入一个课表
    '''
    scheduleDao = ScheduleDao()
    if scheduleDao.insertSchedule(schedule):
        return True
    else:
        raise InsertError(schedule.username)

def deleteSchedule(schedule: Schedule):
    '''
    删除一个课表
    '''
    scheduleDao = ScheduleDao()
    if scheduleDao.deleteSchedule(schedule):
        return True
    else:
        raise DeleteError(schedule.username)

def updateSchedule(schedule: Schedule) -> bool:
    '''
    删除一个课表
    '''
    scheduleDao = ScheduleDao()
    if scheduleDao.updateSchedule(schedule):
        return True
    else:
        raise UpdateError(schedule.username)