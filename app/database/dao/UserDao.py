from typing import Optional

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.MySQLHelper import MySQLHelper
from app.model.po.User import User
from app.util import AuthUtil

tbl_name = 'tbl_user'

col_id = 'u_id'
col_username = 'u_name'
col_password = 'u_password'


class UserDao(MySQLHelper):
    """
    !!!!!!
    uid username hash_pass 存储
    没有 PO，直接在 DAO 加密和验证
    """

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
                    {col_id} INT PRIMARY KEY AUTO_INCREMENT,
                    {col_username} VARCHAR({Config.FMT_USERNAME_MAX}) NOT NULL UNIQUE,
                    {col_password} VARCHAR(150) NOT NULL
                )
            ''')
        except:
            self.db.rollback()
            return False
        finally:
            self.db.commit()
            cursor.close()
        return True

    def queryUserById(self, uid: int) -> Optional[User]:
        """
        根据 uid 查询用户
        """
        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {col_id}, {col_username}, {col_password} 
            FROM {tbl_name}
            WHERE {col_id} = {uid}
        ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            return User(uid=result[0], username=result[1], encrypted_pass=result[2])
        except:
            return None
        finally:
            cursor.close()

    def queryUserByName(self, username: str) -> Optional[User]:
        """
        根据用户名查询用户
        """
        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {col_id}, {col_username}, {col_password}
            FROM {tbl_name}
            WHERE {col_username} = '{username}'
        ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            return User(uid=result[0], username=result[1], encrypted_pass=result[2])
        except:
            return None
        finally:
            cursor.close()

    def checkUserPassword(self, username: str, unencrypted_pass: str) -> (DbStatusType, User):
        """
        检查用户密码正确
        :return: SUCCESS | NOT_FOUND | FAILED (密码不一致) & User
        """
        user = self.queryUserByName(username)
        if user is None:
            return DbStatusType.NOT_FOUND, None

        if AuthUtil.verify_password(password=unencrypted_pass, encrypted_password=user.encrypted_pass):
            return DbStatusType.SUCCESS, user
        else:
            return DbStatusType.FAILED, None

    #######################################################################################################################

    def insertUser(self, username: str, unencrypted_pass: str) -> (DbStatusType, User):
        """
        加密密码并创建新用户
        :return: SUCCESS | FOUNDED | FAILED
        """
        if self.queryUserByName(username):
            return DbStatusType.FOUNDED, None

        encrypted_pass = AuthUtil.encrypt_password(unencrypted_pass)
        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {tbl_name} ({col_username}, {col_password})
                VALUES ('{username}', '{encrypted_pass}')
            ''')

            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None
            return DbStatusType.SUCCESS, self.queryUserById(cursor.lastrowid)
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()
