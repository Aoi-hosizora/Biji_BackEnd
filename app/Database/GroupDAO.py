from app.Utils import PassUtil
from app.Config import Config

from app.Modules.Note.Models.Group import Group
from app.Modules.Note.Exceptions.NotExistError import NotExistError
from app.Modules.Note.Exceptions.ExistError import ExistError

import datetime
import pymysql

class GroupDAO(object):

    tbl_name = "TBL_GROUP"
    
    col_username = "USERNAME"
    col_id = "ID"
    col_name = "NAME"
    col_order = "GORDER" # ORDER preserve word
    col_color = "COLOR"

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
                    {} INT NOT NULL,
                    {} VARCHAR(100) NOT NULL,
                    {} INT NOT NULL,
                    {} VARCHAR(10) NOT NULL,
                    PRIMARY KEY ({}, {}) )""".format(self.tbl_name,
                        self.col_username, self.col_id, self.col_name, self.col_order, self.col_color,
                        self.col_username, self.col_id
                    )
                )
                self.db.commit()
            except:
                self.db.rollback()
    
    def queryUserAllGroups(self, username: str):
        '''
        查询表中用户的所有分组
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(self.tbl_name,
            self.col_username, username
        ))
        sets = []
        rets = self.cursor.fetchall()
        for ret in rets: 
            try:
                group = Group(ret[1], ret[2], ret[3], ret[4])
                sets.append(group)
            except:
                pass
        return sets
    
    def queryUserOneGroup(self, username: str, id: int):
        '''
        查询表中用户的指定分组
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}' AND {} = {}".format(self.tbl_name,
            self.col_username, username, self.col_id, id
        ))
        ret = self.cursor.fetchone()
        try:
            group = Group(ret[1], ret[2], ret[3], ret[4])
            return group
        except:
            return None
    
    def updateUserGroup(self, username: str, group: Group) -> bool:
        '''
        对数据库中用户的指定分组更新
        '''
        if self.queryUserOneGroup(username, group.id) == None:
            raise NotExistError(group.name, isNote=False)

        try:
            id = group.id
            name = group.name
            order = group.order
            color = group.color

            self.cursor.execute("""UPDATE {}
                SET {} = '{}', {} = {}, {} = '{}'
                WHERE {} = '{}' AND {} = {}""".format(self.tbl_name,
                    self.col_name, name, self.col_order, order, self.col_color, color,
                    self.col_username, username, self.col_id, id
                )
            )
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def insertUserGroup(self, username: str, group: Group) -> bool:
        '''
        往数据库添加用户的新分组
        '''
        if not self.queryUserOneGroup(username, group.id) == None:
            raise ExistError(group.name, isNote=False)

        try:
            id = group.id
            name = group.name
            order = group.order
            color = group.color

            self.cursor.execute("""INSERT INTO {}
                ({}, {}, {}, {}, {})
                VALUES ('{}', {}, '{}', {}, '{}')""".format(self.tbl_name,
                    self.col_username, self.col_id, self.col_name, self.col_order, self.col_color,
                    username, id, name, order, color
                )
            )
            self.db.commit()
            if self.queryUserOneGroup(username, group.id) == None:
                return False
            return True
        except:
            self.db.rollback()
            return False
    
    def deleteUserGroup(self, username: str, group: Group) -> bool:
        '''
        删除用户的某个分组
        '''
        if self.queryUserOneGroup(username, group.id) == None:
            raise NotExistError(group.name, isNote=False)
            
        try:
            self.cursor.execute("DELETE FROM {} WHERE {} = '{}' AND {} = {}".format(self.tbl_name,
                self.col_username, username, self.col_id, group.id
            ))
            self.db.commit()
            if self.queryUserOneGroup(username, group.id) == None:
                return True
            return False
        except:
            self.db.rollback()
            return False