from typing import List, Optional

from app.database.DbErrorType import DbErrorType
from app.database.MySQLHelper import MySQLHelper

from app.model.po.StarItem import StarItem


class StarDAO(MySQLHelper):
    tbl_name = 'tbl_star'

    col_username = 'sis_user'
    col_title = 'sis_title'
    col_url = 'sis_url'
    col_content = 'sis_content'

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
                    {self.col_username} VARCHAR(30) NOT NULL,
                    {self.col_url} VARCHAR(200) NOT NULL UNIQUE,
                    {self.col_title} VARCHAR(100) NOT NULL,
                    {self.col_content} VARCHAR(300) NOT NULL,
                    PRIMARY KEY ({self.col_username}, {self.col_url})
                )
            ''')
        except:
            self.db.rollback()
            return False
        finally:
            self.db.commit()
            cursor.close()

        return True

    def queryAllStars(self, username: str) -> List[StarItem]:
        """
        查询所有收藏
        """
        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {self.col_username}, {self.col_url}, {self.col_title}, {self.col_content}
            FROM {self.tbl_name} 
            WHERE {self.col_username} = '{username}'
        ''')

        returns = []
        results = cursor.fetchall()
        for result in results:
            # noinspection PyBroadException
            try:
                returns.append(StarItem(url=result[1], title=result[2], content=result[3]))
            except:
                pass

        cursor.close()
        return returns

    def queryStarByUrl(self, username: str, url: str) -> Optional[StarItem]:
        """
        根据 url 查询收藏
        """
        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {self.col_username}, {self.col_url}, {self.col_title}, {self.col_content}
            FROM {self.tbl_name} 
            WHERE {self.col_username} = '{username}' and {self.col_url} = '{url}'
        ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            return StarItem(url=result[1], title=result[2], content=result[3])
        except:
            return None
        finally:
            cursor.close()

    def insertStar(self, username: str, star: StarItem) -> DbErrorType:
        """
        插入新收藏
        :return: SUCCESS | FOUNDED | FAILED
        """
        if self.queryStarByUrl(username, star.url) is not None:
            return DbErrorType.FOUNDED

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {self.tbl_name} ({self.col_username}, {self.col_url}, {self.col_title}, {self.col_content})
                VALUES ('{username}', {star.url}, '{star.title}', '{star.content}')
            ''')
            self.db.commit()

            if self.queryStarByUrl(username, star.url) is None:
                self.db.rollback()
                return DbErrorType.FAILED

            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()
            cursor.close()

    def deleteStar(self, username: str, url: str) -> DbErrorType:
        """
        删除一个分组
        :return: SUCCESS | NOT_FOUND | FAILED
        """
        if self.queryStarByUrl(username, url) is None:
            return DbErrorType.NOT_FOUND

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                DELETE FROM {self.tbl_name}
                WHERE {self.col_username} = '{username}' AND {self.col_url} = {url}
            ''')

            if self.queryStarByUrl(username, url) is not None:
                self.db.rollback()
                return DbErrorType.FAILED

            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()
            cursor.close()

    def deleteStars(self, username: str, url: List[str]) -> int:
        """
        删除多个分组
        :return: 更新的数目 -1 for error
        """
        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                DELETE FROM {self.tbl_name}
                WHERE {self.col_username} = '{username}' AND {self.col_url} IN ({'"' + '","'.join(url) + '"'})
            ''')
            return cursor.rowcount
        except:
            self.db.rollback()
            return -1
        finally:
            self.db.commit()
            cursor.close()
