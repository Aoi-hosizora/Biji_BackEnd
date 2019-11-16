from typing import List, Optional, Union

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.MySQLHelper import MySQLHelper
from app.model.po.Group import Group, DEF_GROUP


class GroupDao(MySQLHelper):
    tbl_name = 'tbl_group'

    col_user = 'g_user'
    col_id = 'g_id'
    col_name = 'g_name'
    col_order = 'g_order'
    col_color = 'g_color'

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
                    {self.col_user} INT NOT NULL,
                    {self.col_id} INT NOT NULL AUTO_INCREMENT,
                    {self.col_name} VARCHAR({Config.FMT_GROUP_NAME_MAX}) NOT NULL UNIQUE,
                    {self.col_order} INT NOT NULL,
                    {self.col_color} VARCHAR(10) NOT NULL,
                    PRIMARY KEY ({self.col_user}, {self.col_id})
                )
            ''')
        except:
            self.db.rollback()
            return False
        finally:
            self.db.commit()
            cursor.close()
        return True

    def queryAllGroups(self, uid: int) -> List[Group]:
        """
        查询所有分组
        """
        self.processGroups(uid)  # 查询前处理

        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {self.col_user}, {self.col_id}, {self.col_name}, {self.col_order}, {self.col_color}
            FROM {self.tbl_name}
            WHERE {self.col_user} = {uid}
        ''')

        returns = []
        results = cursor.fetchall()
        for result in results:
            # noinspection PyBroadException
            try:
                returns.append(Group(gid=result[1], name=result[2], order=result[3], color=result[4]))
            except:
                pass

        cursor.close()
        return results

    def queryGroupByIdOrName(self, uid: int, gid_name: Union[int, str]) -> Optional[Group]:
        """
        根据 gid 查询分组
        """
        self.processGroups(uid)  # 查询前处理

        cursor = self.db.cursor()
        if isinstance(gid_name, int):
            cursor.execute(f'''
                SELECT {self.col_user}, {self.col_id}, {self.col_name}, {self.col_order}, {self.col_color}
                FROM {self.tbl_name}
                WHERE {self.col_user} = {uid} AND {self.col_id} = {gid_name}
            ''')
        else:
            cursor.execute(f'''
                SELECT {self.col_user}, {self.col_id}, {self.col_name}, {self.col_order}, {self.col_color}
                FROM {self.tbl_name}
                WHERE {self.col_user} = {uid} AND {self.col_name} = '{gid_name}'
            ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            return Group(gid=result[1], name=result[2], order=result[3], color=result[4])
        except:
            return None
        finally:
            cursor.close()

    def queryDefaultGroup(self, uid: int) -> Group:
        """
        查询默认分组
        """
        return self.queryGroupByIdOrName(uid, DEF_GROUP.name)

    #######################################################################################################################

    def insertGroup(self, uid: int, group: Group) -> (DbStatusType, Group):
        """
        插入新分组 (name, color) SUCCESS | FOUNDED | FAILED | DUPLICATE
        """
        if self.queryGroupByIdOrName(uid, group.id) is not None:  # 已存在
            return DbStatusType.FOUNDED, None
        if self.queryGroupByIdOrName(uid, group.name) is not None:  # 名字重复
            return DbStatusType.DUPLICATE, None

        self.processGroups(uid)  # 插入前处理
        group.order = len(self.queryAllGroups(uid))  # 顺序最后

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {self.tbl_name} (
                    {self.col_user}, {self.col_name}, {self.col_order}, {self.col_color}
                )
                VALUES (
                    {uid}, '{group.name}', {group.order}, '{group.color}'
                )
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None

            cursor.execute(f'''SELECT MAX({self.col_id} FROM {self.tbl_name}''')
            new_group_id = int(cursor.fetchone()[0])
            new_group = self.queryGroupByIdOrName(uid, new_group_id)
            return DbStatusType.SUCCESS, new_group
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

    def updateGroup(self, uid: int, group: Group) -> (DbStatusType, Group):
        """
        更新分组 (name, order, color) SUCCESS | NOT_FOUND | DEFAULT | FAILED | DUPLICATE
        """
        if self.queryGroupByIdOrName(uid, group.id) is None:  # 不存在
            return DbStatusType.NOT_FOUND, None
        if self.queryGroupByIdOrName(uid, group.name) is not None:  # 名字重复
            return DbStatusType.DUPLICATE, None
        self.processGroups(uid)  # 更新前处理

        # 修改默认分组名
        defGroup = self.queryDefaultGroup(uid)
        if group.id == defGroup.id and group.name != defGroup:
            return DbStatusType.DEFAULT, None

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                UPDATE {self.tbl_name} 
                WHERE {self.col_user} = {uid} AND {self.col_id} = {group.id}
                SET {self.col_name} = '{group.name}', {self.col_order} = {group.order}, {self.col_color} = '{group.color}'
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None

            cursor.execute(f'''SELECT MAX({self.col_id} FROM {self.tbl_name}''')
            new_group_id = int(cursor.fetchone()[0])
            new_group = self.queryGroupByIdOrName(uid, new_group_id)
            return DbStatusType.SUCCESS, new_group
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

    def deleteGroup(self, uid: int, gid: int) -> DbStatusType:
        """
        删除一个分组 SUCCESS | NOT_FOUND | DEFAULT | FAILED
        """
        if self.queryGroupByIdOrName(uid, gid) is None:  # 不存在
            return DbStatusType.NOT_FOUND

        # 删除默认分组
        if gid == self.queryDefaultGroup(uid).id:
            return DbStatusType.DEFAULT

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                DELETE FROM {self.tbl_name}
                WHERE {self.col_user} = {uid} AND {self.col_id} = {gid}
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED

            self.processGroups(uid)  # 删除后处理
            return DbStatusType.SUCCESS
        except:
            self.db.rollback()
            return DbStatusType.FAILED
        finally:
            self.db.commit()
            cursor.close()

    ####################################################################################

    def processGroups(self, uid: int):
        """
        操作前后 处理顺序和默认分组
        """

        # 使用 Raw Json 防止递归
        def query(name: str) -> bool:
            cursor = self.db.cursor()
            cursor.execute(f'''
                SELECT * FROM {self.tbl_name}
                WHERE {self.col_user} = {uid} AND {self.col_name} = {name}
            ''')
            return cursor.rowcount != 0

        def insert(g: Group):
            cursor = self.db.cursor()
            # noinspection PyBroadException
            try:
                cursor.execute(f'''
                    INSERT INTO {self.tbl_name} ({self.col_user}, {self.col_id}, {self.col_name}, {self.col_order}, {self.col_color})
                    VALUES ({uid}, {g.id}, '{g.name}', {g.order}, '{g.color}')
                ''')
            except:
                self.db.rollback()
            finally:
                self.db.commit()
                cursor.close()

        def queryAll() -> List[Group]:
            cursor = self.db.cursor()
            cursor.execute(f'''
                SELECT {self.col_user}, {self.col_id}, {self.col_name}, {self.col_order}, {self.col_color}
                FROM {self.tbl_name}
                WHERE {self.col_user} = {uid}
            ''')
            returns = []
            results = cursor.fetchall()
            for result in results:
                # noinspection PyBroadException
                try:
                    returns.append(Group(gid=result[1], name=result[2], order=result[3], color=result[4]))
                except:
                    pass
            cursor.close()
            return results

        def update(g: Group):
            cursor = self.db.cursor()
            # noinspection PyBroadException
            try:
                cursor.execute(f'''
                    UPDATE {self.tbl_name} 
                    WHERE {self.col_user} = {uid} AND {self.col_id} = {g.id}
                    SET {self.col_order} = '{g.order}'
                 ''')
            except:
                self.db.rollback()
            finally:
                self.db.commit()
                cursor.close()

        # 插入默认分组
        if query(DEF_GROUP.name) is None:
            insert(DEF_GROUP)

        # 处理顺序 小到大
        groups = sorted(queryAll(), key=lambda key: key.order)
        for idx, group in enumerate(groups):
            if group.order != idx:
                group.order = idx
                update(group)
