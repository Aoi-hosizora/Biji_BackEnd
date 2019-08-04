from app.Config import Config

from app.Modules.File.Models.File import File
from app.Modules.File.Exceptions.ExistError import ExistError
from app.Modules.File.Exceptions.FileNotExistError import FileNotExistError

import pymysql


class FileDAO(object):
    tbl_name = "TBL_FILE"
    col_username = "USERNAME"
    col_foldername = "FOLDERNAME"
    col_filename = "FILENAME"
    col_filepath = "FILEPATH"

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
                    {} VARCHAR(200) NOT NULL,
                    {} VARCHAR(200) NOT NULL,
                    {} VARCHAR(2000) NOT NULL,
                    PRIMARY KEY ( {}, {}, {} )
                ) CHARACTER SET = utf8;
                """.format(self.tbl_name, self.col_username,
                            self.col_foldername, self.col_filename,
                            self.col_filepath, self.col_username,
                            self.col_foldername, self.col_filename))
                self.db.commit()
            except:
                self.db.rollback()

    def queryAllFiles(self):
        '''
        查询表中所有文件
        '''
        self.cursor.execute("SELECT * FROM {}".format(self.tbl_name))
        rets = self.cursor.fetchall()
        set = []
        for ret in rets:
            set.append(File(ret[0], ret[1], ret[2], ret[3]))
        return set

    def queryFiles(self, username: str, foldername: str):
        '''
        查询指定用户名和文件夹的表项
        '''
        self.cursor.execute("SELECT * FROM {} WHERE USERNAME='{}' AND FOLDERNAME='{}'"
                            .format(self.tbl_name, username, foldername))
        rets = self.cursor.fetchall()
        set = []
        for ret in rets:
            set.append(File(ret[0], ret[1], ret[2], ret[3]))
        return set

    def queryOneFile(self, username: str, foldername: str, filename: str):
        '''
        查询指定文件
        '''
        self.cursor.execute("SELECT * FROM {} WHERE USERNAME='{}' AND FOLDERNAME='{}'"
                            "AND FILENAME='{}'".format(self.tbl_name, username, foldername, filename))
        ret = self.cursor.fetchone()

        try:
            return File(ret[0], ret[1], ret[2], ret[3])
        except:
            return None

    def insertFile(self, file: File) -> bool:
        '''
        插入到数据库
        '''
        username = file.username
        foldername = file.foldername
        filename = file.filename
        filepath = file.filepath

        if self.queryOneFile(username, foldername, filename) != None:
            raise ExistError(foldername, filename)

        try:
            self.cursor.execute("INSERT INTO {} ({}, {}, {}, {}) VALUES ('{}', '{}', '{}', '{}')".format(
                self.tbl_name, self.col_username, self.col_foldername, self.col_filename, self.col_filepath,
                username, foldername, filename, filepath
            ))
            self.db.commit()
            if self.queryOneFile(username, foldername, filename) == None:
                return False
            return True
        except:
            self.db.rollback()
            return False

    def deleteFile(self, file: File) -> bool:
        '''
        删除文件
        '''
        username = file.username
        foldername = file.foldername
        filename = file.filename

        if self.queryOneFile(username, foldername, filename) == None:
            raise FileNotExistError(filename)

        try:
            self.cursor.execute("DELETE FROM {} WHERE USERNAME == '{}' AND FOLDERNAME='{}'"
                                "AND FILENAME='{}'".format(self.tbl_name, username, foldername, filename))
            self.db.commit()
            if self.queryOneFile(username, foldername, filename) != None:
                return False
            return True
        except:
            self.db.rollback()
            return False
