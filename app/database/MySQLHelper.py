import pymysql

from app.config import Config


class MySQLHelper(object):

    def __init__(self):
        """
        统一建立数据库
        """
        self.db = pymysql.connect(
            host=Config.MySQL_Host,
            port=Config.MySQL_Port,
            user=Config.MySQL_User,
            passwd=Config.MySQL_Pass,
            db=Config.MySQL_Db,
            charset='utf8'
        )
        self.create_tbl()

    def __del__(self):
        self.db.close()

    def create_tbl(self) -> bool:
        """
        判断是否存在并建表 Must Override
        :return: 建表过程是否错误
        """
        pass
