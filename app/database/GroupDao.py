from typing import List

from app.database.DbErrorType import DbErrorType
from app.database.DbHelper import DbHelper

from app.model.po.Group import Group, DEF_GROUP


class GroupDao(DbHelper):
    tbl_name = "tbl_group"

    col_username = "g_user"
    col_id = "g_id"
    col_name = "g_name"
    col_order = "g_order"
    col_color = "g_color"

    def __init__(self):
        super().__init__()

    def create_tbl(self) -> bool:
        """
        判断是否存在并建表
        """
        # noinspection PyBroadException
        try:
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.tbl_name} (
                    {self.col_username} VARCHAR(30) NOT NULL,
                    {self.col_id} INT AUTO_INCREMENT,
                    {self.col_name} VARCHAR(100) NOT NULL UNIQUE,
                    {self.col_order} INT NOT NULL,
                    {self.col_color} VARCHAR(10) NOT NULL,
                    PRIMARY KEY ({self.col_username}, {self.col_id})
                )
            ''')
        except:
            self.db.rollback()
            return False
        finally:
            self.db.commit()
        return True

    def queryAllGroups(self, username: str) -> List[Group]:
        """
        查询所有分组
        """
        self.processGroups(username)  # 查询前处理

        self.cursor.execute(f'''
            SELECT {self.col_username, self.col_id, self.col_name, self.col_order, self.col_color}
            FROM {self.tbl_name}
            WHERE {self.col_username} = '{username}'
        ''')

        returns = []
        results = self.cursor.fetchall()
        for result in results:
            # noinspection PyBroadException
            try:
                returns.append(Group(gid=result[1], name=result[2], order=result[3], color=result[4]))
            except:
                pass
        return results

    def queryGroupById(self, username: str, gid: int) -> Group or None:
        """
        根据 gid 查询分组
        """
        self.processGroups(username)  # 查询前处理

        self.cursor.execute(f'''
            SELECT {self.col_username, self.col_id, self.col_name, self.col_order, self.col_color}
            FROM {self.tbl_name}
            WHERE {self.col_username} = '{username}' AND {self.col_id} = {gid}
        ''')
        result = self.cursor.fetchone()
        # noinspection PyBroadException
        try:
            return Group(gid=result[1], name=result[2], order=result[3], color=result[4])
        except:
            return None

    def queryGroupByName(self, username: str, name: str) -> Group or None:
        """
        根据 name 查询分组
        """
        self.processGroups(username)  # 查询前处理

        self.cursor.execute(f'''
            SELECT {self.col_username, self.col_id, self.col_name, self.col_order, self.col_color}
            FROM {self.tbl_name}
            WHERE {self.col_username} = '{username}' AND {self.col_name} = {name}
        ''')
        result = self.cursor.fetchone()
        # noinspection PyBroadException
        try:
            return Group(gid=result[1], name=result[2], order=result[3], color=result[4])
        except:
            return None

    def queryDefaultGroup(self, username: str) -> Group:
        """
        查询默认分组
        """
        return self.queryGroupByName(username=username, name=DEF_GROUP.name)

    def insertGroup(self, username: str, group: Group) -> DbErrorType:
        """
        插入新分组
        :return: SUCCESS | FOUNDED | FAILED
        """
        if self.queryGroupById(username, group.id) is not None:
            return DbErrorType.FOUNDED
        # noinspection PyBroadException
        try:
            self.cursor.execute(f'''
                INSERT INTO {self.tbl_name} (
                    {self.col_username}, {self.col_id}, {self.col_name}, {self.col_order}, {self.col_color}
                )
                VALUES (
                    '{username}', {group.id}, '{group.name}', {group.order}, '{group.color}'
                )
            ''')
            self.db.commit()

            if self.queryGroupById(username, group.id) is None:
                self.db.rollback()
                return DbErrorType.FAILED

            self.processGroups(username)  # 插入后处理
            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()

    def updateGroup(self, username: str, group: Group) -> DbErrorType:
        """
        更新分组 除了 gid
        :return: SUCCESS | NOT_FOUND | FAILED
        """
        if self.queryGroupById(username, group.id) is None:
            return DbErrorType.NOT_FOUND
        # noinspection PyBroadException
        try:
            self.cursor.execute(f'''
                UPDATE {self.tbl_name}
                SET {self.col_name} = '{group.name}', {self.col_order} = '{group.order}', {self.col_color} = {group.color}
            ''')

            newGroup = self.queryGroupById(username, group.id)
            if newGroup.name != group.name or newGroup.order != group.order or newGroup.color != group.color:
                self.db.rollback()
                return DbErrorType.FAILED

            self.processGroups(username)  # 更新后处理
            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()

    def deleteGroup(self, username: str, gid: int) -> DbErrorType:
        """
        删除一个分组
        :return: SUCCESS | NOT_FOUND | FAILED
        """
        if self.queryGroupById(username, gid) is None:
            return DbErrorType.NOT_FOUND
        # noinspection PyBroadException
        try:
            self.cursor.execute(f'''
                DELETE FROM {self.tbl_name}
                WHERE {self.col_username} = '{username}' AND {self.col_id} = {gid}
            ''')

            if self.queryGroupById(username, gid) is not None:
                self.db.rollback()
                return DbErrorType.FAILED

            self.processGroups(username)  # 删除后处理
            return DbErrorType.SUCCESS
        except:
            self.db.rollback()
            return DbErrorType.FAILED
        finally:
            self.db.commit()

    def processGroups(self, username):
        """
        操作前后 处理顺序和默认分组
        TODO 调用位置
        """
        groups = self.queryAllGroups(username)

        if self.queryDefaultGroup(username) is None:
            self.insertGroup(username, DEF_GROUP)

        groups = sorted(groups, key=lambda key: key.order)  # 小到大
        for idx, group in enumerate(groups):
            if group.order != idx:
                group.order = idx
                self.updateGroup(username, group)
