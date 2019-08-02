from app.Utils import PassUtil
from app.Config import Config

from app.Modules.Star.Models.StarItem import StarItem
from app.Modules.Star.Exceptions.NotExistError import NotExistError
from app.Modules.Star.Exceptions.ExistError import ExistError

import datetime
import pymysql

class StarDAO(object):

    tbl_name = "TBL_STAR"
    
    col_username = "USERNAME"
    col_title = "TITLE"
    col_url = "URL"
    col_content = "CONTENT"

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
                    {} VARCHAR(100) NOT NULL,
                    {} VARCHAR(200) NOT NULL,
                    {} VARCHAR(300),
                    PRIMARY KEY ({}, {}) )""".format(self.tbl_name,
                        self.col_username, self.col_title, self.col_url, self.col_content,
                        self.col_username, self.col_url
                    )
                )
                self.db.commit()
            except:
                self.db.rollback()
    
    def queryUserAllStars(self, username: str):
        '''
        查询表中用户的所有收藏
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(self.tbl_name,
            self.col_username, username
        ))
        sets = []
        rets = self.cursor.fetchall()
        for ret in rets: 
            try:
                star = StarItem(ret[1], ret[2], ret[3])
                sets.append(star)
            except:
                pass
        return sets
    
    def queryUserOneStar(self, username: str, url: str):
        '''
        查询表中用户的指定收藏
        '''
        self.cursor.execute("SELECT * FROM {} WHERE {} = '{}' AND {} = '{}'".format(self.tbl_name,
            self.col_username, username, self.col_url, url
        ))
        ret = self.cursor.fetchone()
        try:
            star = StarItem(ret[1], ret[2], ret[3])
            return star
        except:
            return None

    def insertUserStar(self, username: str, star: StarItem) -> bool:
        '''
        往数据库添加用户的新收藏
        '''
        if not self.queryUserOneStar(username, star.url) == None:
            raise ExistError(star.title)

        try:
            title = star.title
            url = star.url
            content = star.content

            self.cursor.execute("""INSERT INTO {}
                ({}, {}, {}, {})
                VALUES ('{}', '{}', '{}', '{}')""".format(self.tbl_name,
                    self.col_username, self.col_title, self.col_url, self.col_content,
                    username, title, url, content
                )
            )
            self.db.commit()
            if self.queryUserOneStar(username, star.url) == None:
                return False
            return True
        except:
            self.db.rollback()
            return False
    
    def deleteUserStar(self, username: str, star: StarItem) -> bool:
        '''
        删除用户的某个分组
        '''
        if self.queryUserOneStar(username, star.url) == None:
            raise NotExistError(star.title)
            
        try:
            self.cursor.execute("DELETE FROM {} WHERE {} = '{}' AND {} = '{}'".format(self.tbl_name,
                self.col_username, username, self.col_url, star.url
            ))
            self.db.commit()
            if not self.queryUserOneStar(username, star.url) == None:
                return False
            return True
        except:
            self.db.rollback()
            return False