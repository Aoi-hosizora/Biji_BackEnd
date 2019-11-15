from app.config import Config
from app.controller.file.exception.FileClassNotExistError import FileClassNotExistError

from app.model.po.Document import Document
from app.controller.file.exception.FileExistError import ExistError
from app.controller.file.exception.FileNotExistError import FileNotExistError

import pymysql


class DocumentDao(object):
    tbl_name = "TBL_FILE"
    col_username = "USERNAME"
    col_id = "ID"
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
                    {} INT NOT NULL,
                    {} VARCHAR(200) NOT NULL,
                    {} VARCHAR(200) NOT NULL,
                    {} VARCHAR(2000) NOT NULL,
                    PRIMARY KEY ( {}, {}, {}, {} )
                ) CHARACTER SET = utf8;
                """.format(self.tbl_name, self.col_username, self.col_id, self.col_foldername,
                            self.col_filename, self.col_filepath,
                            self.col_username, self.col_id,
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
            set.append(Document(ret[0], ret[1], ret[2], ret[3], ret[4]))
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
            set.append(Document(ret[0], ret[1], ret[2], ret[3], ret[4]))
        return set

    def queryFilesByUsername(self, username: str):
        '''
        查询指定用户名的表项
        '''
        self.cursor.execute("SELECT * FROM {} WHERE USERNAME='{}'"
                            .format(self.tbl_name, username))
        rets = self.cursor.fetchall()
        set = []
        for ret in rets:
            set.append(Document(ret[0], ret[1], ret[2], ret[3], ret[4]))
        return set

    def queryOneFile(self, username: str, foldername: str, filename: str, id: int):
        '''
        查询指定文件
        '''
        self.cursor.execute("SELECT * FROM {} WHERE USERNAME='{}' AND FOLDERNAME='{}'"
                            "AND FILENAME='{}' AND ID={}".format(self.tbl_name, username, foldername, filename, id))
        ret = self.cursor.fetchone()

        try:
            return Document(ret[0], ret[1], ret[2], ret[3], ret[4])
        except:
            return None

    def insertFile(self, file: Document) -> bool:
        '''
        插入到数据库
        '''
        username = file.username
        id = file.id
        foldername = file.foldername
        filename = file.filename
        filepath = file.filepath

        if self.queryOneFile(username, foldername, filename, id) != None:
            raise ExistError(foldername, filename)

        try:
            self.cursor.execute("INSERT INTO {} ({}, {}, {}, {}, {}) VALUES ('{}', '{}', '{}', '{}', {})".format(
                self.tbl_name, self.col_username, self.col_foldername, self.col_filename, self.col_filepath, self.col_id,
                username, foldername, filename, filepath, id
            ))
            self.db.commit()
            if self.queryOneFile(username, foldername, filename, id) == None:
                return False
            return True
        except Exception as ex:
            print(ex)
            self.db.rollback()
            return False

    def deleteFile(self, file: Document) -> bool:
        '''
        删除文件
        '''
        username = file.username
        id = file.id
        foldername = file.foldername
        filename = file.filename

        if self.queryOneFile(username, foldername, filename, id) == None:
            raise FileNotExistError(filename)

        try:
            self.cursor.execute("DELETE FROM {} WHERE USERNAME = '{}' AND FOLDERNAME='{}'"
                                "AND FILENAME='{}' AND ID={}".format(self.tbl_name, username, foldername, filename, id))
            self.db.commit()
            if self.queryOneFile(username, foldername, filename, id) != None:
                return False
            return True
        except:
            self.db.rollback()
            return False

    def deleteFileByClass(self, username: str, fileClassName: str) -> bool:
        '''
        删除文件
        '''

        if len(self.queryFiles(username, fileClassName)) == 0:
            raise FileClassNotExistError(fileClassName)

        try:
            self.cursor.execute("DELETE FROM {} WHERE USERNAME = '{}' AND FOLDERNAME='{}'"
                                .format(self.tbl_name, username, fileClassName))
            self.db.commit()
            if len(self.queryFiles(username, fileClassName)) != 0:
                return False
            return True
        except Exception as e:
            print(str(e))
            self.db.rollback()
            return False
