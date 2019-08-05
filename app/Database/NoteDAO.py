from app.Utils import PassUtil
from app.Config import Config

from app.Modules.Note.Models.Note import Note
from app.Modules.Note.Exceptions.NotExistError import NotExistError
from app.Modules.Note.Exceptions.ExistError import ExistError

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
    
    def queryUserAllNotes(self, username: str) -> [Note]:
        '''
        查询表中用户的所有笔记
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(self.tbl_name,
            self.col_username, username
        ))
        sets = []
        rets = self.cursor.fetchall()
        for ret in rets: 
            try:
                note = Note(ret[1], ret[2], ret[3], ret[4], ret[5], ret[6])
                sets.append(note)
            except:
                pass
        return sets
        
    def queryUserOneNote(self, username: str, id: int):
        '''
        查询表中用户的指定笔记
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}' AND {} = {}".format(self.tbl_name,
            self.col_username, username, self.col_id, id
        ))
        ret = self.cursor.fetchone()
        try:
            note = Note(ret[1], ret[2], ret[3], ret[4], ret[5], ret[6])
            return note
        except:
            return None
    
    def updateUserNote(self, username: str, note: Note) -> bool:
        '''
        对数据库中用户的指定笔记更新
        '''
        if self.queryUserOneNote(username, note.id) == None:
            raise NotExistError(note.title)

        try:
            id = note.id
            title = note.title
            content = note.content
            groupid = note.group_id
            create_time = note.create_time
            update_time = note.update_time

            self.cursor.execute("""UPDATE {}
                SET {} = '{}', {} = '{}', {} = {}, {} = '{}', {} = '{}'
                WHERE {} = '{}' AND {} = {}""".format(self.tbl_name,
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

    def insertUserNote(self, username: str, note: Note) -> bool:
        '''
        往数据库添加用户的新笔记
        '''
        if not self.queryUserOneNote(username, note.id) == None:
            raise ExistError(note.title)

        # TODO 可能要删除
        
        try:
            id = note.id
            title = note.title
            content = note.content
            groupid = note.group_id
            create_time = note.create_time
            update_time = note.update_time

            self.cursor.execute("""INSERT INTO {}
                ({}, {}, {}, {}, {}, {}, {})
                VALUES ('{}', {}, '{}', '{}', {}, '{}', '{}')""".format(self.tbl_name,
                    self.col_username, self.col_id, self.col_title, self.col_content,
                    self.col_groupid, self.col_create_time, self.col_update_time,
                    username, id, title, content, groupid, create_time, update_time
                )
            )
            self.db.commit()
            if self.queryUserOneNote(username, note.id) == None:
                return False
            return True
        except:
            self.db.rollback()
            return False
    
    def deleteUserNote(self, username: str, note: Note) -> bool:
        '''
        删除用户的某条笔记
        '''
        if self.queryUserOneNote(username, note.id) == None:
            raise NotExistError(note.title)

        try:
            self.cursor.execute("DELETE FROM {} WHERE {} = '{}' AND {} = {}".format(self.tbl_name,
                self.col_username, username, self.col_id, note.id
            ))
            self.db.commit()
            if not self.queryUserOneNote(username, note.id) == None:
                return False
            return True
        except:
            self.db.rollback()
            return False