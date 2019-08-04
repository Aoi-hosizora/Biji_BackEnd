from app.Config import Config

from app.Modules.Schedule.Models.Schedule import Schedule
from app.Modules.Schedule.Exceptions.ExistError import ExistError
from app.Modules.Schedule.Exceptions.ScheduleNotExistError import ScheduleNotExistError

import pymysql


class ScheduleDAO(object):
    tbl_name = "TBL_SCHEDULE"
    col_username = "USERNAME"
    col_schedulejson = "SCHEDULEJSON"

    def __init__(self):
        self.db = pymysql.connect(
            host=Config.MySQL_Host,
            port=Config.MySQL_Port,
            user=Config.MySQL_User,
            passwd=Config.MySQL_Pass,
            db=Config.MySQL_Db,
            charset='utf8'
        )
        self.cursor = self.db.cursor()
        self.result = self.createTbl()

    def __del__(self):
        self.db.close()

    def createTbl(self):
        '''
        判断表是否存在，并且创建表
        '''
        self.cursor.execute("SHOW TABLES LIKE '{}'".format(self.tbl_name))
        if self.cursor.fetchone() == None:
            try:
                self.cursor.execute("""CREATE TABLE {} (
                    {} VARCHAR(30) NOT NULL PRIMARY KEY,
                    {} VARCHAR(5000) NOT NULL
                ) CHARACTER SET = utf8;
                """.format(self.tbl_name, self.col_username, self.col_schedulejson))
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                return str(e)


    def querySchedule(self, username: str):
        '''
        查询指定用户名的表项
        '''
        self.cursor.execute("SELECT * FROM {} WHERE USERNAME='{}'"
                            .format(self.tbl_name, username))
        ret = self.cursor.fetchone()
        try:
            return Schedule(ret[0], ret[1])
        except:
            return None


    def insertSchedule(self, schedule: Schedule) -> bool:
        '''
        插入到数据库
        '''
        username = schedule.username
        schedulejson = schedule.schedulejson

        if self.querySchedule(username) != None:
            raise ExistError(username)

        try:
            self.cursor.execute("INSERT INTO {} ({}, {}) VALUES ('{}', '{}')".format(
                self.tbl_name, self.col_username, self.col_schedulejson,
                username, schedulejson))
            self.db.commit()
            if self.querySchedule(username) == None:
                return False
            return True
        except:
            self.db.rollback()
            return False

    def deleteSchedule(self, schedule: Schedule) -> bool:
        '''
        删除课表
        '''
        username = schedule.username
        schedulejson = schedule.schedulejson

        if self.querySchedule(username) == None:
            raise ScheduleNotExistError(username)

        try:
            self.cursor.execute("DELETE FROM {} WHERE USERNAME = '{}'".format(self.tbl_name, username))
            self.db.commit()
            if self.querySchedule(username) != None:
                return False
            return True
        except:
            self.db.rollback()
            return False

    def updateSchedule(self, schedule: Schedule) -> bool:
        '''
        对数据库中用户的课表更新
        '''
        username = schedule.username
        if self.querySchedule(username) == None:
            raise ScheduleNotExistError(username)

        try:
            self.cursor.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}'"
                                .format(self.tbl_name, self.col_schedulejson, schedule.schedulejson,
                                        self.col_username, username))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
