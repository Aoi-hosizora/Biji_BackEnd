from app.Utils import PassUtil
from app.Config import Config

import datetime
import pymysql

class GroupDAO(object):

    tbl_name = "TBL_GROUP"
    
    col_username = "USERNAME"
    col_id = "ID"
    col_name = "NAME"
    col_order = "GORDER"
    col_color = "COLOR"

    def __init__(self):
        self.db = pymysql.connect(
            host=Config.MySQL_Host,
            port=Config.MySQL_Port,
            user=Config.MySQL_User,
            passwd=Config.MySQL_Pass,
            db=Config.MySQL_Tbl,
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
    
    def queryUserAllNotes(self, username: str):
        '''
        查询表中用户的所有分组
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(self.tbl_name,
            self.col_username, username
        ))
        return self.cursor.fetchall()
    
    def queryUserOneNote(self, username: str, id: int):
        '''
        查询表中用户的指定分组
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} == '{}' AND {} == '{}'".format(self.tbl_name,
            self.col_username, username, self.col_id, id
        ))
        return self.cursor.fetchall()
    
    def updateUserNote(self, username: str, id: int, name: str, order: int, color: str) -> bool:
        '''
        对数据库中用户的指定分组更新
        '''
        try:
            self.cursor.execute("""UPDATE {}
                SET {} = '{}', {} = '{}', {} = '{}'
                WHERE {} == '{}' AND {} == '{}'""".format(self.tbl_name,
                    self.col_name, name, self.col_order, order, self.col_color, color,
                    self.col_username, username, self.col_id, id
                )
            )
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def insertUserGroup(self, username: str, id: int, name: str, order: int, color: str) -> bool:
        '''
        往数据库添加用户的新分组
        '''
        try:
            self.cursor.execute("""INSERT INTO {}
                ({}, {}, {}, {}, {})
                VALUES ('{}', '{}', '{}', '{}', '{}')""".format(self.tbl_name,
                    self.col_username, self.col_id, self.col_name, self.col_order, self.col_color,
                    username, id, name, order, color
                )
            )
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
    
    def deleteUserGroup(self, username: str, id: int) -> bool:
        '''
        删除用户的某个分组
        '''
        try:
            self.cursor.execute("DELETE FROM {} WHERE {} == '{}' AND {} == {}".format(self.tbl_name,
                self.col_username, username, self.col_id, id
            ))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False