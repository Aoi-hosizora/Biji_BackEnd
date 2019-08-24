from app.Config import Config

from app.Modules.File.Models.FileClass import FileClass
from app.Modules.File.Exceptions.FileClassNotExistError import FileClassNotExistError
from app.Modules.File.Exceptions.FileClassExistError import FileClassExistError

import pymysql

class FileClassDAO(object):

    tbl_name = "TBL_FILECLASS"

    col_username = "USERNAME"
    col_id = "ID"
    col_name = "NAME"

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
                    PRIMARY KEY ({}, {}) )""".format(self.tbl_name,
                        self.col_username, self.col_id, self.col_name, self.col_username, self.col_id
                    )
                )
                self.db.commit()
            except:
                self.db.rollback()
    
    def queryUserAllFileClasses(self, username: str):
        '''
        查询表中用户的所有文件分类
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(self.tbl_name,
            self.col_username, username
        ))
        sets = []
        rets = self.cursor.fetchall()
        for ret in rets: 
            try:
                fileClass = FileClass(ret[1], ret[2]) # id, name
                sets.append(fileClass)
            except:
                pass
        return sets
    
    def queryUserOneFileClass(self, username: str, id: int):
        '''
        查询表中指定文件分类
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}' AND {} = {}".format(self.tbl_name,
            self.col_username, username, self.col_id, id
        ))
        ret = self.cursor.fetchone()
        try:
            fileClass = FileClass(ret[1], ret[2])
            return fileClass
        except:
            return None
    
    def updateUserFileClass(self, username: str, fileClass: FileClass) -> bool:
        '''
        对数据库中用户的指定文件分类更新
        '''
        if self.queryUserOneFileClass(username, fileClass.id) == None:
            raise FileClassNotExistError(fileClass.name)

        try:
            id = fileClass.id
            name = fileClass.name

            self.cursor.execute("""UPDATE {}
                SET {} = '{}' WHERE {} = '{}' AND {} = {}""".format(self.tbl_name,
                    self.col_name, name, self.col_username, username, self.col_id, id
                )
            )
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def insertUserFileClass(self, username: str, fileClass: FileClass) -> bool:
        '''
        往数据库添加新的文件分类
        '''
        if not self.queryUserOneFileClass(username, fileClass.id) == None:
            raise FileClassExistError(fileClass.name)

        try:
            id = fileClass.id
            name = fileClass.name

            self.cursor.execute("""INSERT INTO {}
                ({}, {}, {})
                VALUES ({}, '{}', '{}')""".format(self.tbl_name,
                    self.col_id, self.col_username, self.col_name,
                    id, username, name
                )
            )
            self.db.commit()
            if self.queryUserOneFileClass(username, fileClass.id) == None:
                return False
            return True
        except:
            self.db.rollback()
            return False
    
    def deleteUserFileClass(self, username: str, fileClass: FileClass) -> bool:
        '''
        删除某个文件分类
        '''
        if self.queryUserOneFileClass(username, fileClass.id) == None:
            raise FileClassNotExistError(fileClass.name)
            
        try:
            self.cursor.execute("DELETE FROM {} WHERE {} = '{}' AND {} = {}".format(self.tbl_name,
                self.col_username, username, self.col_id, fileClass.id
            ))
            self.db.commit()
            if self.queryUserOneFileClass(username, fileClass.id) == None:
                return True
            return False
        except:
            self.db.rollback()
            return False
