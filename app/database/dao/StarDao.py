from typing import List, Optional, Union

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.MySQLHelper import MySQLHelper
from app.model.po.StarItem import StarItem

tbl_name = 'tbl_star'

col_user = 'sis_user'
col_id = 'sis_id'
col_url = 'sis_url'
col_title = 'sis_title'
col_content = 'sis_content'


class StarDao(MySQLHelper):

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
                    {col_user} INT NOT NULL,
                    {col_id} INT PRIMARY KEY AUTO_INCREMENT,
                    {col_url} VARCHAR(500) NOT NULL,
                    {col_title} VARCHAR({Config.FMT_STAR_TITLE_MAX}) NOT NULL,
                    {col_content} VARCHAR({Config.FMT_STAR_CONTENT_MAX})
                )
            ''')
        except:
            self.db.rollback()
            return False
        finally:
            self.db.commit()
            cursor.close()

        return True

    def queryAllStars(self, uid: int) -> List[StarItem]:
        """
        查询所有收藏
        """
        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {col_user}, {col_id}, {col_url}, {col_title}, {col_content}
            FROM {tbl_name} 
            WHERE {col_user} = {uid}
        ''')

        returns = []
        results = cursor.fetchall()
        for result in results:
            # noinspection PyBroadException
            try:
                returns.append(StarItem(sid=result[1], url=result[2], title=result[3], content=result[4]))
            except:
                pass

        cursor.close()
        return returns

    def queryStarByIdOrUrl(self, uid: int, sid_url: Union[int, str]) -> Optional[StarItem]:
        """
        根据 sid / url 查询收藏
        """
        cursor = self.db.cursor()
        if isinstance(sid_url, int):
            cursor.execute(f'''
                SELECT {col_user}, {col_id}, {col_url}, {col_title}, {col_content}
                FROM {tbl_name} 
                WHERE {col_user} = {uid} and {col_id} = {sid_url}
            ''')
        else:
            cursor.execute(f'''
                SELECT {col_user}, {col_id}, {col_url}, {col_title}, {col_content}
                FROM {tbl_name} 
                WHERE {col_user} = {uid} and {col_url} = '{sid_url}'
            ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            return StarItem(sid=result[1], url=result[2], title=result[3], content=result[4])
        except:
            return None
        finally:
            cursor.close()

    #######################################################################################################################

    def insertStar(self, uid: int, star: StarItem) -> (DbStatusType, StarItem):
        """
        插入新收藏 (url, title, content) SUCCESS | FOUNDED | FAILED
        """
        if self.queryStarByIdOrUrl(uid, star.id) is not None:  # 已存在
            return DbStatusType.FOUNDED, None

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {tbl_name} ({col_user}, {col_url}, {col_title}, {col_content})
                VALUES ({uid}, '{star.url}', '{star.title}', '{star.content}')
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None
            return DbStatusType.SUCCESS, self.queryStarByIdOrUrl(uid, cursor.lastrowid)
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

    def deleteStars(self, uid: int, ids: List[int]) -> int:
        """
        删除多个分组
        :return: 删除的数目 -1 for error
        """
        if len(ids) == 0:
            return 0
        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                DELETE FROM {tbl_name}
                WHERE {col_user} = {uid} AND {col_id} IN ({', '.join([str(sid) for sid in ids])})
            ''')
            return cursor.rowcount
        except:
            self.db.rollback()
            return -1
        finally:
            self.db.commit()
            cursor.close()
