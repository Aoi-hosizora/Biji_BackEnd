from typing import List, Optional, Union

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.MySQLHelper import MySQLHelper
from app.model.po.Group import Group, DEF_GROUP

tbl_name = 'tbl_group'

col_user = 'g_user'
col_id = 'g_id'
col_name = 'g_name'
col_order = 'g_order'
col_color = 'g_color'


class GroupDao(MySQLHelper):

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
                    {col_name} VARCHAR({Config.FMT_GROUP_NAME_MAX}) NOT NULL UNIQUE,
                    {col_order} INT NOT NULL,
                    {col_color} VARCHAR(10) NOT NULL
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
            SELECT {col_user}, {col_id}, {col_name}, {col_order}, {col_color}
            FROM {tbl_name}
            WHERE {col_user} = {uid}
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
        return returns

    def queryGroupByIdOrName(self, uid: int, gid_name: Union[int, str]) -> Optional[Group]:
        """
        根据 gid 查询分组
        """
        self.processGroups(uid)  # 查询前处理

        cursor = self.db.cursor()
        if isinstance(gid_name, int):
            cursor.execute(f'''
                SELECT {col_user}, {col_id}, {col_name}, {col_order}, {col_color}
                FROM {tbl_name}
                WHERE {col_user} = {uid} AND {col_id} = {gid_name}
            ''')
        else:
            cursor.execute(f'''
                SELECT {col_user}, {col_id}, {col_name}, {col_order}, {col_color}
                FROM {tbl_name}
                WHERE {col_user} = {uid} AND {col_name} = '{gid_name}'
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

        group.order = len(self.queryAllGroups(uid))  # 顺序最后

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {tbl_name} (
                    {col_user}, {col_name}, {col_order}, {col_color}
                )
                VALUES (
                    {uid}, '{group.name}', {group.order}, '{group.color}'
                )
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None
            return DbStatusType.SUCCESS, self.queryGroupByIdOrName(uid, int(cursor.lastrowid))
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
        sameIdGroup = self.queryGroupByIdOrName(uid, group.id)
        if sameIdGroup is None:  # 不存在
            return DbStatusType.NOT_FOUND, None
        sameNameGroup = self.queryGroupByIdOrName(uid, group.name)
        if sameNameGroup and sameNameGroup.id != group.id:  # 名字重复
            return DbStatusType.DUPLICATE, None
        # 沒更新
        if group.name == sameIdGroup.name and group.order == sameIdGroup.order and group.color == sameIdGroup.color:
            return DbStatusType.SUCCESS, sameIdGroup

        # 修改默认分组名
        defGroup = self.queryDefaultGroup(uid)
        if group.id == defGroup.id and group.name != defGroup.name:
            return DbStatusType.DEFAULT, None

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                UPDATE {tbl_name} 
                SET {col_name} = '{group.name}', {col_order} = {group.order}, {col_color} = '{group.color}'
                WHERE {col_user} = {uid} AND {col_id} = {group.id}
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None

            self.db.commit()  # !!!
            self.processGroups(uid)  # 更新后处理
            return DbStatusType.SUCCESS, self.queryGroupByIdOrName(uid, group.id)
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

    def updateGroupsOrder(self, uid: int, ids: List[int], orders: List[int]) -> (DbStatusType, int):
        """
        更新分组顺序 (order) SUCCESS | FAILED
        """
        # 修改默认分组名
        defGroup = self.queryDefaultGroup(uid)

        count = 0
        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            for gid, order in zip(ids, orders):
                if gid == defGroup.id:
                    continue
                print(gid, order)
                cursor.execute(f'''SELECT {col_order} FROM {tbl_name} WHERE {col_user} = {uid} AND {col_id} = {gid}''')
                moto_order = cursor.fetchone()[0]  # 修改
                if order != moto_order:
                    cursor.execute(f'''
                        UPDATE {tbl_name}
                        SET {col_order} = {order}
                        WHERE {col_user} = {uid} AND {col_id} = {gid}
                    ''')
                    if cursor.rowcount == 0:
                        self.db.rollback()
                        return DbStatusType.FAILED, None
                    count += cursor.rowcount
        except Exception as ex:
            print(ex)
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

        self.processGroups(uid)  # 更新后处理
        return DbStatusType.SUCCESS, count

    def deleteGroup(self, uid: int, gid: int, toDefault: bool) -> DbStatusType:
        """
        删除一个分组 SUCCESS | NOT_FOUND | DEFAULT | FAILED
        對應修改筆記
        """
        from app.database.dao import NoteDao

        if self.queryGroupByIdOrName(uid, int(gid)) is None:  # 不存在
            return DbStatusType.NOT_FOUND

        # 删除默认分组
        def_group = self.queryDefaultGroup(uid)
        if gid == def_group.id:
            return DbStatusType.DEFAULT

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            # 對應筆記
            cursor.execute(f'''
                SELECT COUNT(*) FROM {NoteDao.tbl_name} 
                WHERE {NoteDao.col_user} = {uid} AND {NoteDao.col_group_id} = {gid}
            ''')
            note_len = cursor.fetchone()[0]
            if note_len != 0:  # 有對應筆記
                if toDefault:  # 修改為默認
                    cursor.execute(f'''
                        UPDATE {NoteDao.tbl_name}
                        SET {NoteDao.col_group_id} = {def_group.id}
                        WHERE {NoteDao.col_user} = {uid} AND {NoteDao.col_group_id} = {gid}
                    ''')
                    if cursor.rowcount == 0:
                        self.db.rollback()
                        return DbStatusType.FAILED
                else:  # 刪除
                    cursor.execute(f'''
                        DELETE FROM {NoteDao.tbl_name}
                        WHERE {NoteDao.col_user} = {uid} AND {NoteDao.col_group_id} = {gid}
                    ''')
                    if cursor.rowcount == 0:
                        self.db.rollback()
                        return DbStatusType.FAILED
            # 删除分組
            cursor.execute(f'''
                DELETE FROM {tbl_name}
                WHERE {col_user} = {uid} AND {col_id} = {gid}
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED

            self.db.commit()  # !!!
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
                SELECT * FROM {tbl_name}
                WHERE {col_user} = {uid} AND {col_name} = '{name}'
            ''')
            count = cursor.rowcount
            cursor.close()
            return count != 0

        def insert(g: Group):
            cursor = self.db.cursor()
            # noinspection PyBroadException
            try:
                cursor.execute(f'''
                    INSERT INTO {tbl_name} ({col_user}, {col_id}, {col_name}, {col_order}, {col_color})
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
                SELECT {col_user}, {col_id}, {col_name}, {col_order}, {col_color}
                FROM {tbl_name}
                WHERE {col_user} = {uid}
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
            self.db.commit()
            return returns

        def update(gid: int, order: int):
            cursor = self.db.cursor()
            # noinspection PyBroadException
            try:
                cursor.execute(f'''
                    UPDATE {tbl_name} 
                    SET {col_order} = {order}
                    WHERE {col_user} = {uid} AND {col_id} = {gid}
                 ''')
            except:
                self.db.rollback()
            finally:
                self.db.commit()
                cursor.close()

        # 插入默认分组
        if not query(DEF_GROUP.name):
            insert(DEF_GROUP)

        # 处理顺序 小到大
        groups = sorted(queryAll(), key=lambda k: k.order)
        for idx, group in enumerate(groups):
            if group.name != DEF_GROUP.name and group.order != idx:
                update(group.id, idx)
