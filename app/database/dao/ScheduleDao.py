from app.database.DbErrorType import DbErrorType
from app.database.MySQLHelper import MySQLHelper


class ScheduleDao(MySQLHelper):
    tbl_name = "tbl_schedule"

    col_user = "sc_user"
    col_json = "sc_json"

    def __init__(self):
        super().__init__()

    def create_tbl(self) -> bool:
        """
        判断是否存在并建表
        """
        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.tbl_name} (
                    {self.col_user} INT NOT NULL PRIMARY KEY,
                    {self.col_json} TEXT DEFAULT ('')
                )
            ''')
        except:
            self.db.rollback()
            return False
        finally:
            self.db.commit()
            cursor.close()

        return True

    def querySchedule(self, uid: int) -> str:
        """
        用户课程表
        """
        cursor = self.db.cursor()
        cursor.execute(f'''SELECT {self.col_user}, {self.col_json} FROM {self.tbl_name} WHERE {self.col_user} = {uid}''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            return result[1]
        except:
            return ''
        finally:
            cursor.close()

    def updateSchedule(self, uid: int, data: str) -> DbErrorType:
        """
        更新课程表
        :return: SUCCESS | FAILED
        """
        db_data = self.querySchedule(uid)
        if db_data == data:  # Not Modify
            return DbErrorType.SUCCESS

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            if db_data == '':  # New
                cursor.execute(f'''INSERT INTO {self.tbl_name} ({self.col_user}, {self.col_json}) VALUES ({uid}, {data})''')
            else:
                cursor.execute(f'''UPDATE {self.tbl_name} WHERE {self.col_user} = {uid} SET {self.col_json} = {data}''')

            if cursor.rowcount == 0:
                self.db.rollback()
                return DbErrorType.FAILED
            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()
            cursor.close()

    def deleteSchedule(self, uid: int) -> DbErrorType:
        """
        删除课表
        :return: SUCCESS | NOT_FOUND | FAILED
        """
        if self.querySchedule(uid) == '':
            return DbErrorType.NOT_FOUND

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''DELETE FROM {self.tbl_name} WHERE {self.col_user} = {uid}''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbErrorType.FAILED
            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()
            cursor.close()
