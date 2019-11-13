from app.util import PassUtil
from app.config import Config

import pymysql


class UserDAO(object):
    tbl_name = "TBL_USER"
    col_username = "USERNAME"
    col_password = "PASSWORD"

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

    def createTbl(self):
        """
        判断表是否存在，并且创建表
        """
        self.cursor.execute("SHOW TABLES LIKE '{}'".format(self.tbl_name))
        if self.cursor.fetchone() is None:
            try:
                self.cursor.execute("""CREATE TABLE {} (
                    {} VARCHAR(30) NOT NULL PRIMARY KEY,
                    {} VARCHAR(120) NOT NULL
                )""".format(self.tbl_name, self.col_username, self.col_password))
                self.db.commit()
            except:
                self.db.rollback()

    def queryAllUsers(self):
        """
        查询表中所有用户
        """
        self.cursor.execute("SELECT * FROM {}".format(self.tbl_name))
        return self.cursor.fetchall()

    def queryUser(self, username: str):
        """
        查询指定用户名的表项
        """
        self.cursor.execute("SELECT * FROM {} WHERE USERNAME='{}'".format(self.tbl_name, username))
        return self.cursor.fetchone()

    def insertUser(self, username: str, password: str) -> bool:
        """
        加密密码，并且插入到数据库
        """
        psd_encrypted = PassUtil.hash_password(password)
        try:
            self.cursor.execute("INSERT INTO {} ({}, {}) VALUES ('{}', '{}')".format(
                self.tbl_name, self.col_username, self.col_password, username, psd_encrypted
            ))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def deleteUser(self, username: str) -> bool:
        """
        删除用户
        """
        try:
            self.cursor.execute("DELETE FROM {} WHERE {} = '{}'".format(self.tbl_name, self.col_username, username))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def checkUserPassword(self, username: str, password: str) -> bool:
        """
        判断密码是否正确
        """
        user = self.queryUser(username)
        if user == None:
            return False
        else:
            return PassUtil.verify_password(password, user[1])
