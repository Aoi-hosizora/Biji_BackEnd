from app.Utils import PassUtil
from app.Config import Config

import datetime
import pymysql

class NoteDAO(object):

    tbl_name = "TBL_NOTE"
    
    col_username = "USERNAME"
    col_id = "ID"
    col_title = "TITLE"
    col_content = "CONTENT"
    col_groupid = "GROUPID"
    col_create_time = "CREATE_TIME"
    col_update_time = "UPDATE_TIME"

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
                    {} TEXT,
                    {} INT NOT NULL,
                    {} DATETIME NOT NULL,
                    {} DATETIME NOT NULL,
                    PRIMARY KEY ({}, {}) )""".format(self.tbl_name,
                        self.col_username, self.col_id, self.col_title, self.col_content,
                        self.col_groupid, self.col_create_time, self.col_update_time,
                        self.col_username, self.col_id
                    )
                )
                self.db.commit()
                return True
            except:
                self.db.rollback()
                return False
    
    def queryUserAllNotes(self, username: str):
        '''
        查询表中用户的所有笔记
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(self.tbl_name,
            self.col_username, username
        ))
        return self.cursor.fetchall()
    
    def queryUserOneNote(self, username: str, id: int):
        '''
        查询表中用户的指定笔记
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} == '{}' AND {} == '{}'".format(self.tbl_name,
            self.col_username, username, self.col_id, id
        ))
        return self.cursor.fetchall()
    
    def updateUserNote(self, username: str, id: int, title: str, content: str, groupid: str, create_time: datetime, update_time: datetime) -> bool:
        '''
        对数据库中用户的指定笔记更新
        '''
        try:
            self.cursor.execute("""UPDATE {}
                SET {} = '{}', {} = '{}', {} = '{}', {} = '{}', {} = '{}'
                WHERE {} == '{}' AND {} == '{}'""".format(self.tbl_name,
                    self.col_title, title, self.col_content, content, self.col_groupid, groupid,
                    self.col_create_time, create_time, self.col_update_time, update_time,
                    self.col_username, username, self.col_id, id
                )
            )
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False


    def insertUserNote(self, username: str, id: int, title: str, content: str, groupid: str, create_time: datetime, update_time: datetime) -> bool:
        '''
        往数据库添加用户的新笔记
        '''
        try:
            self.cursor.execute("""INSERT INTO {}
                ({}, {}, {}, {}, {}, {}, {})
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(self.tbl_name,
                    self.col_username, self.col_id, self.col_title, self.col_content,
                    self.col_groupid, self.col_create_time, self.col_update_time,
                    username, id, title, content, groupid, create_time, update_time
                )
            )
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
    
    def deleteUserNote(self, username: str, id: int) -> bool:
        '''
        删除用户的某条笔记
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