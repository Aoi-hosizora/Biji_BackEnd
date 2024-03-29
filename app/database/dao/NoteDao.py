from typing import List, Optional

from app.config.Config import Config
from app.database.DbStatusType import DbStatusType
from app.database.MySQLHelper import MySQLHelper
from app.database.dao.GroupDao import GroupDao
from app.model.po.Note import Note

tbl_name = 'tbl_note'

col_user = 'n_user'
col_id = 'n_id'
col_title = 'n_title'
col_content = 'n_content'
col_group_id = 'n_group_id'
col_create_time = 'n_create_time'
col_update_time = 'n_update_time'


class NoteDao(MySQLHelper):

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
                    {col_title} VARCHAR ({Config.FMT_NOTE_TITLE_MAX}) NOT NULL,
                    {col_content} TEXT,
                    {col_group_id} INT NOT NULL,
                    {col_create_time} DATETIME NOT NULL,
                    {col_update_time} DATETIME NOT NULL
                )
            ''')
        except:
            self.db.rollback()
            return False
        finally:
            self.db.commit()
            cursor.close()
        return True

    def queryAllNotes(self, uid: int) -> List[Note]:
        """
        查询所有笔记
        """
        return self.queryAllNotesByGroupId(uid, -1)

    def queryAllNotesByGroupId(self, uid: int, gid: int) -> List[Note]:
        """
        根据分组查询笔记
        :param uid: 用户id
        :param gid: 所有分组为 -1
        """
        cursor = self.db.cursor()
        if gid == -1:
            cursor.execute(f'''
                SELECT {col_user}, {col_id}, {col_title}, {col_content}, {col_group_id}, {col_create_time}, {col_update_time}
                FROM {tbl_name} 
                WHERE {col_user} = {uid}
            ''')
        else:
            cursor.execute(f'''
                SELECT {col_user}, {col_id}, {col_title}, {col_content}, {col_group_id}, {col_create_time}, {col_update_time}
                FROM {tbl_name} 
                WHERE {col_user} = {uid} AND {col_group_id} = {gid}
            ''')

        returns = []
        results = cursor.fetchall()
        for result in results:
            # noinspection PyBroadException
            try:
                group = GroupDao().queryGroupByIdOrName(uid, gid_name=int(result[4]))
                if group is None:
                    group = GroupDao().queryDefaultGroup(uid)
                returns.append(Note(nid=result[1], title=result[2], content=result[3], group=group, create_time=result[5], update_time=result[6]))
            except:
                pass

        cursor.close()
        return returns

    def queryNoteById(self, uid: int, nid: int) -> Optional[Note]:
        """
        根据 nid 查询笔记
        :return: nullable
        """
        cursor = self.db.cursor()
        cursor.execute(f'''
            SELECT {col_user}, {col_id}, {col_title}, {col_content}, {col_group_id}, {col_create_time}, {col_update_time}
            FROM {tbl_name}
            WHERE {col_user} = {uid} AND {col_id} = {nid}
        ''')
        result = cursor.fetchone()
        # noinspection PyBroadException
        try:
            group = GroupDao().queryGroupByIdOrName(uid, gid_name=int(result[4]))
            if group is None:
                group = GroupDao().queryDefaultGroup(uid)
            return Note(nid=result[1], title=result[2], content=result[3], group=group, create_time=result[5], update_time=result[6])
        except:
            return None
        finally:
            cursor.close()

    #######################################################################################################################

    def insertNote(self, uid: int, note: Note) -> (DbStatusType, Note):
        """
        插入新笔记 (title, content, group_id, ct, ut) SUCCESS | FOUNDED | FAILED
        """
        if self.queryNoteById(uid, note.id):  # 已存在
            return DbStatusType.FOUNDED, None

        if not GroupDao().queryGroupByIdOrName(uid=uid, gid_name=note.group.id):  # 分组不存在
            note.group = GroupDao().queryDefaultGroup(uid=uid)

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                INSERT INTO {tbl_name} (
                    {col_user}, {col_title}, {col_content}, {col_group_id}, {col_create_time}, {col_update_time}
                )
                VALUES ({uid}, '{note.title}', '{note.content}', {note.group.id}, '{note.create_time}', '{note.update_time}')
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None
            return DbStatusType.SUCCESS, self.queryNoteById(uid, nid=cursor.lastrowid)
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

    def updateNote(self, uid: int, note: Note) -> (DbStatusType, Note):
        """
        更新笔记 (title, content, group_id, ut) SUCCESS | NOT_FOUND | FAILED
        """
        sameIdNote = self.queryNoteById(uid, note.id)
        if not sameIdNote:  # 不存在
            return DbStatusType.NOT_FOUND, None

        if not GroupDao().queryGroupByIdOrName(uid=uid, gid_name=note.group.id):  # 分组不存在
            note.group = GroupDao().queryDefaultGroup(uid=uid)

        # 沒更新
        if note.title == sameIdNote.title and note.content == sameIdNote.content and note.group.id == sameIdNote.group.id:
            return DbStatusType.SUCCESS, sameIdNote

        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                UPDATE {tbl_name} 
                SET {col_title} = '{note.title}', {col_content} = '{note.content}', 
                    {col_group_id} = {note.group.id}, {col_update_time} = '{note.update_time}'
                WHERE {col_user} = {uid} AND {col_id} = {note.id}
            ''')
            if cursor.rowcount == 0:
                self.db.rollback()
                return DbStatusType.FAILED, None
            return DbStatusType.SUCCESS, self.queryNoteById(uid, note.id)
        except:
            self.db.rollback()
            return DbStatusType.FAILED, None
        finally:
            self.db.commit()
            cursor.close()

    def deleteNotes(self, uid: int, ids: List[int]) -> int:
        """
        删除多个笔记
        :return: 删除的条数 -1 for error
        """
        if len(ids) == 0:
            return 0
        cursor = self.db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(f'''
                DELETE FROM {tbl_name}
                WHERE {col_user} = {uid} AND {col_id} IN ({', '.join([str(nid) for nid in ids])})
            ''')
            return cursor.rowcount
        except:
            self.db.rollback()
            return -1
        finally:
            self.db.commit()
            cursor.close()
