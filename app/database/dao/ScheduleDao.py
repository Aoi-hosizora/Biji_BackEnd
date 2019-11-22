from app.database.DbStatusType import DbStatusType
from app.database.MySQLHelper import MySQLHelper

tbl_name = "tbl_schedule"

col_user = "sc_user"
col_json = "sc_json"
col_week = "sc_week"


class ScheduleDao(MySQLHelper):

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
                CREATE TABLE IF NOT EXISTS {tbl_name} (
                    {col_user} INT NOT NULL PRIMARY KEY,
                    {col_json} TEXT DEFAULT (''),
                    {col_week} INT DEFAULT (1)
                )
            ''')
        except:
            self.db.rollback()
            return False
        finally:
            self.db.commit()
            cursor.close()

        return True

    def querySchedule(self, uid: int) -> (str, int):
        """
        用户课程表
        """
        cursor = self.db.cursor()
        cursor.execute(f'''SELECT {col_user}, {col_json}, {col_week} FROM {tbl_name} WHERE {col_user} = {uid}''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            return result[1], result[2]
        except:
            return '', -1
        finally:
            cursor.close()

    #######################################################################################################################

    def updateSchedule(self, uid: int, data: str, week: int) -> (DbStatusType, str, int):
        """
        更新课程表
        :return: SUCCESS | FAILED
        """
        db_data, db_week = self.querySchedule(uid)
        if db_data == data and db_week == week:  # Not Modify
            return DbStatusType.SUCCESS, db_data, db_week

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            if db_data == '':  # New
                cursor.execute(f'''INSERT INTO {tbl_name} ({col_user}, {col_json}, {col_week}) VALUES ({uid}, '{data}', {week})''')
            else:
                cursor.execute(f'''UPDATE {tbl_name} SET {col_json} = '{data}', {col_week} = {week} WHERE {col_user} = {uid}''')

            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, '', -1
            data, week = self.querySchedule(uid)
            return DbStatusType.SUCCESS, data, week
        except:
            self.db.rollback()
            return DbStatusType.FAILED, '', -1
        finally:
            self.db.commit()
            cursor.close()

    def deleteSchedule(self, uid: int) -> (DbStatusType, str, int):
        """
        删除课表
        :return: SUCCESS | NOT_FOUND | FAILED
        """
        db_data, db_week = self.querySchedule(uid)
        if db_data == '':
            return DbStatusType.NOT_FOUND, '', -1

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''DELETE FROM {tbl_name} WHERE {col_user} = {uid}''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, '', -1
            return DbStatusType.SUCCESS, db_data, db_week
        except:
            self.db.rollback()
            return DbStatusType.FAILED, '', -1
        finally:
            self.db.commit()
            cursor.close()
