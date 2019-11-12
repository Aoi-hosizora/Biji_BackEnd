from app.util import PassUtil
from app.config import Config

from app.module.log.Models.Log import Log

import datetime
import pymysql

class LogDAO(object):

    tbl_name = "TBL_LOG"
    
    col_username = "USERNAME"
    col_module = "MODULE"
    col_time = "TIME"

    mod_note = "Note"
    mod_group = "Group"
    mod_star = "Star"
    mod_file_class = "FileClass"
    mod_file = "File"
    mod_schedule = "Schedule"
    mods = [mod_note, mod_group, mod_star, mod_file_class, mod_file, mod_schedule]

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
        self.createTbl()

    def __del__(self):
        self.db.close()

    def createTbl(self) -> bool:
        '''
        判断表是否存在，并且创建表
        '''
        self.cursor.execute("SHOW TABLES LIKE '{}'".format(self.tbl_name))
        if self.cursor.fetchone() == None:
            try:
                self.cursor.execute("""CREATE TABLE {} (
                    {} VARCHAR(30) NOT NULL,
                    {} VARCHAR(10) NOT NULL,
                    {} DATETIME NOT NULL,
                    PRIMARY KEY ({}, {}) )""".format(self.tbl_name,
                        self.col_username, self.col_module, self.col_time,
                        self.col_username, self.col_module
                    )
                )
                self.db.commit()
            except:
                self.db.rollback()

    def createLogLine(self, username: str, module: str) -> bool:
        '''
        创建 Log 行
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}' AND {} = '{}'".format(self.tbl_name,
            self.col_username, username, self.col_module, module
        ))
        if self.cursor.fetchone() == None:
            try:
                self.cursor.execute( """INSERT INTO {}
                    ({}, {}, {})
                    VALUES ('{}', '{}', '{}')""".format(self.tbl_name,
                        self.col_username, self.col_module, self.col_time,
                        username, module, datetime.datetime.now()
                    )
                )
                self.db.commit()
                return True
            except:
                self.db.rollback()
                return False
    
    def createAllLogLine(self, username: str):
        '''
        创建所有 Log 行
        '''
        for module in self.mods:
            self.createLogLine(username, module)

    def queryUserAllLogs(self, username: str) -> [Log]:
        '''
        查询表中用户的所有更新日志
        '''
        self.createAllLogLine(username)
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(self.tbl_name,
            self.col_username, username
        ))
        sets = []
        rets = self.cursor.fetchall()
        for ret in rets: 
            try:
                log = Log(ret[1], ret[2])
                sets.append(log)
            except:
                pass
        return sets
    
    def queryUserOneLog(self, username: str, module: str) -> Log:
        '''
        查询表中用户的指定日志
        '''
        self.createLogLine(username, module)
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}' AND {} = '{}'".format(self.tbl_name,
            self.col_username, username, self.col_module, module
        ))
        ret = self.cursor.fetchone()
        try:
            log = Log(ret[1], ret[2])
            return log
        except:
            return None

    def updateUserLog(self, username: str, module: str, ut: datetime = datetime.datetime.now()) -> bool:
        '''
        对数据库中用户的指定日志更新
        '''
        try:
            self.createLogLine(username, module)
            self.cursor.execute("""UPDATE {} SET {} = '{}'
                WHERE {} = '{}' AND {} = '{}'""".format(self.tbl_name,
                    self.col_time, ut,
                    self.col_username, username, self.col_module, module
                )
            )
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False