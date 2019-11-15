from typing import Optional

from app.database.DbErrorType import DbErrorType
from app.database.MySQLHelper import MySQLHelper
from app.model.po.User import User
from app.util import AuthUtil


class UserDao(MySQLHelper):
    """
    !!!!!!
    uid username hash_pass 存储
    没有 PO，直接在 DAO 加密和验证
    """
    tbl_name = 'tbl_user'

    col_id = 'u_id'
    col_username = 'u_name'
    col_password = 'u_password'

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
                    {self.col_id} INT PRIMARY KEY AUTO_INCREMENT,
                    {self.col_username} VARCHAR(30) UNIQUE,
                    {self.col_password} VARCHAR(120) NOT NULL
                )
            ''')
        except:
            self.db.rollback()
            return False
        finally:
            self.db.commit()
            cursor.close()
        return True

    # def queryAllUsers(self) -> List[User]:
    #     """
    #     查询所有用户
    #     """
    #     cursor = self.db.cursor()
    #     cursor.execute(f'''
    #         SELECT {self.col_id}, {self.col_username}, {self.col_password} FROM {self.tbl_name}
    #     ''')
    #
    #     returns = []
    #     results = cursor.fetchall()
    #     for result in results:
    #         # noinspection PyBroadException
    #         try:
    #             returns.append(User(uid=result[0], username=result[1], encrypted_pass=result[2]))
    #         except:
    #             pass
    #
    #     cursor.close()
    #     return returns

    def queryUserById(self, uid: int) -> Optional[User]:
        """
        根据 uid 查询用户
        """
        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {self.col_id}, {self.col_username}, {self.col_password} 
            FROM {self.tbl_name}
            WHERE {self.col_id} = '{uid}'
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
            SELECT {self.col_id}, {self.col_username}, {self.col_password}
            FROM {self.tbl_name}
            WHERE {self.col_username} = '{username}'
        ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            return User(uid=result[0], username=result[1], encrypted_pass=result[2])
        except:
            return None
        finally:
            cursor.close()

    def checkUserPassword(self, username: str, unencrypted_pass: str) -> (DbErrorType, User):
        """
        检查用户密码正确
        :return: SUCCESS | NOT_FOUND | FAILED (密码不一致) & User
        """
        user = self.queryUserByName(username)
        if user is None:
            return DbErrorType.NOT_FOUND, None

        if AuthUtil.verify_password(password=unencrypted_pass, encrypted_password=user.encrypted_pass):
            return DbErrorType.SUCCESS, user
        else:
            return DbErrorType.FAILED, None

    #########################################################################################################################

    def insertUser(self, username: str, unencrypted_pass: str) -> DbErrorType:
        """
        加密密码并创建新用户
        :return: SUCCESS | FOUNDED | FAILED
        """
        encrypted_pass = AuthUtil.encrypt_password(unencrypted_pass)
        if self.queryUserByName(username) is not None:
            return DbErrorType.FOUNDED

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {self.tbl_name} ({self.col_username}, {self.col_password})
                VALUES ('{username}', '{encrypted_pass}')
            ''')
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

    # def deleteUser(self, username: str) -> DbErrorType:
    #     """
    #     删除用户
    #     :return: SUCCESS | NOT_FOUND | FAILED
    #     """
    #     if self.queryUserByName(username) is None:
    #         return DbErrorType.NOT_FOUND
    #
    #     cursor = self.db.cursor()
    #     # noinspection PyBroadException
    #     try:
    #         cursor.execute(f'''DELETE FROM {self.tbl_name} WHERE {self.col_username} = '{username}' ''')
    #         if cursor.rowcount == 0:
    #             self.db.rollback()
    #             return DbErrorType.FAILED
    #         return DbErrorType.SUCCESS
    #     except:
    #         self.db.rollback()
    #         return DbErrorType.FAILED
    #     finally:
    #         self.db.commit()
    #         cursor.close()
